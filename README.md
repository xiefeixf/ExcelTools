# ExcelTools 使用说明

## 项目简介
ExcelTools 是一个自动化工具，用于将 Excel 表格数据转换为 TypeScript 类型定义和数据文件。适用于游戏开发、前端项目中配置表的代码生成场景，提升开发效率与数据一致性。

## 目录结构
```
ExcelTools/
├── script/              # Python 源代码
│   ├── build_exe.py          # 构建可执行程序脚本
│   ├── excelToTs.py          # Excel 转 TypeScript 接口定义
│   ├── excelToTsData.py      # Excel 转 TypeScript 数据（Map 格式）
│   ├── generateGlobalConfig.py # 生成全局配置
│   ├── run_all.py            # 主程序入口（一键执行所有转换）
│   └── requirements.txt      # Python 依赖包列表
├── assets/              # 资源配置文件
│   └── Init/
│       └── Config/      # 生成的 TypeScript 配置文件
│           ├── ConfigData.ts   # 配置数据（Map 格式）
│           ├── ConfigType.ts   # 配置类型定义
│           └── GlobalConfig.ts # 全局配置及查询方法
├── dist/                # 打包生成的可执行文件
│   ├── ExcelTools.exe        # 统一的主程序
│   └── assets/               # 资源文件夹
├── routePath.txt        # 路径配置文件
└── README.md            # 项目说明文档
```

## 核心功能

### 1. Excel → TypeScript 类型定义
自动读取 Excel 表头结构，生成 TypeScript 接口定义。

**Excel 格式要求：**
- 第 1 行：字段名（如：id, name, hp）
- 第 2 行：类型声明（number/string/boolean/array/json）
- 第 3 行：中文注释
- 第 4 行：示例值（用于推断 array/json 的具体类型）
- 第 5 行起：实际数据

**生成的 TypeScript：**
```typescript
export interface XXXInfo {
  /** ID */
  id: number;
  /** 名称 */
  name: string;
  /** 生命值 */
  hp: number;
  /** 位置坐标 */
  pos: { x: number, y: number, z: number };
}
```

### 2. Excel → TypeScript 数据文件
将 Excel 数据转换为 Map 格式，使用第一列字段作为 key，支持 O(1) 快速查找。

**生成的 TypeScript：**
```typescript
export const XXXData = new Map([
  [1, { id: 1, name: "战士", hp: 100 }],
  [2, { id: 2, name: "法师", hp: 80 }]
]);
```

**特性：**
- ✅ 自动识别第一列字段作为 Map 的 key
- ✅ 支持数字和字符串类型的 key
- ✅ 智能过滤主键为空的无效数据
- ✅ 自动清理数字格式（1.0 → 1，保留 1.5）
- ✅ 支持 x/y/z 坐标合并为 pos 对象

### 3. 全局配置生成
整合类型定义和数据文件，生成统一的 GlobalConfig 及便捷的查询方法。

**生成的 TypeScript：**
```typescript
import { XXXInfo } from "./ConfigType";
import { XXXData } from "./ConfigData";

export const GlobalConfig: {
  XXX: Map<string | number, XXXInfo>;
} = {
  XXX: XXXData as Map<string | number, XXXInfo>
};

// 通用查询方法
export function getConfigById(table: keyof typeof GlobalConfig, id: number | string) {
  const map = GlobalConfig[table];
  if (!(map instanceof Map)) return undefined;
  return map.get(id);
}

// 专用查询方法
export function getXXXById(id: number | string): XXXInfo | undefined {
  const map = GlobalConfig.XXX;
  if (!(map instanceof Map)) return undefined;
  return map.get(id);
}
```

## 使用方法

### 方式一：使用可执行文件（推荐）

1. **运行统一主程序**
```bash
cd dist
.\ExcelTools.exe
```

这将自动按顺序执行：
1. TypeScript 类型定义生成
2. TypeScript 数据文件生成（Map 格式）
3. 全局配置文件生成

### 方式二：使用 Python 源码运行

1. **安装依赖**
```bash
pip install -r script/requirements.txt
```

2. **运行主程序**
```bash
python script/run_all.py
```

或单独运行各个模块：
```bash
python script/excelToTs.py          # 生成类型定义
python script/excelToTsData.py      # 生成数据文件
python script/generateGlobalConfig.py  # 生成全局配置
```

## 配置说明

### routePath.txt 配置文件

在项目根目录创建 `routePath.txt`，定义输入输出路径：

```
INPUT_PATH=./                                    # Excel 文件输入目录
OUTPUT_TS_PATH=../assets/Init/Config/ConfigType.ts      # 类型定义输出路径
OUTPUT_DATA_PATH=../assets/Init/Config/ConfigData.ts    # 数据文件输出路径
GLOBAL_CONFIG_PATH=../assets/Init/Config/GlobalConfig.ts # 全局配置输出路径
```

如果不存在该文件，程序将使用默认路径。

## 打包说明

如需重新生成 EXE 可执行文件：

```bash
python script/build_exe.py
```

这将：
- 自动安装 PyInstaller（如果未安装）
- 清理旧的构建文件
- 打包生成统一的 `ExcelTools.exe`
- 复制 resources 到输出目录

## 注意事项

### ⚠️ 必需条件
- **routePath.txt**：必须在项目根目录创建该配置文件（或使用默认路径）
- **assets 目录**：必须存在且与脚本或可执行文件同级
- **Excel 格式**：必须严格遵守 5 行规范（字段名、类型、注释、示例值、数据）

### ⚠️ 数据有效性
- **主键唯一性**：确保第一列字段的值在每行中是唯一的，避免数据覆盖
- **空值处理**：主键为 null、空字符串的行会被自动跳过，并输出警告信息
- **数字格式**：浮点数会自动转换为整数（如 1.0 → 1），小数保持不变（如 1.5）

### ⚠️ TypeScript 兼容性
- 生成的 Map 语法符合 ES6 标准，使用数组元组形式 `[key, value]`
- 需要 TypeScript 3.0+ 支持 Map 类型
- 建议在 tsconfig.json 中启用 `esModuleInterop`

## 常见问题

### Q: 为什么我的数据没有被导出？
A: 检查以下几点：
1. Excel 格式是否符合 5 行规范
2. 第一列主键是否为空（空值会被自动跳过）
3. 是否保存了 Excel 文件（临时文件 ~$ 开头会被忽略）

### Q: 如何更改输入输出路径？
A: 修改 `routePath.txt` 配置文件中的路径设置。

### Q: 可以单独使用某个功能吗？
A: 可以。直接运行单个脚本（如 `excelToTs.py`）即可只执行对应功能。

### Q: 生成的 Map 如何使用？
A: 参考下面的使用示例。

## 使用示例

### 基础使用
```typescript
// 导入全局配置
import { GlobalConfig, getCharacterById } from "./GlobalConfig";

// 方式一：使用专用方法
const char1 = getCharacterById(1);

// 方式二：使用通用方法
const char2 = getConfigById('Character', 1);

// 方式三：直接访问 Map
const char3 = GlobalConfig.Character.get(1);

// 检查是否存在
if (GlobalConfig.Character.has(1)) {
  console.log("角色存在");
}
```

### 遍历数据
```typescript
// 遍历所有角色
for (const [id, character] of GlobalConfig.Character.entries()) {
  console.log(`ID: ${id}, Name: ${character.name}`);
}

// 获取所有 keys
const ids = Array.from(GlobalConfig.Character.keys());

// 获取所有 values
const characters = Array.from(GlobalConfig.Character.values());
```

## 版本历史

### v2.0
- ✅ 支持 Map 格式数据导出（替代数组格式）
- ✅ 使用第一列字段作为 Map 的 key
- ✅ 自动过滤主键为空的无效数据
- ✅ 智能清理数字格式（去除不必要的小数点）
- ✅ 统一的 ExcelTools.exe 主程序
- ✅ 增强的错误处理和警告提示

### v1.0
- 初始版本，支持基础的 Excel 转 TypeScript 功能
