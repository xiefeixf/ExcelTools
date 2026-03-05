# ExcelTools 使用说明

## 目录结构
```
ExcelTools/
├── script/              # Python 源代码
│   ├── build_exe.py          # 构建可执行程序脚本
│   ├── excelToTs.py          # Excel 转 TypeScript 接口定义
│   ├── excelToTsData.py      # Excel 转 TypeScript 数据
│   ├── generateGlobalConfig.py # 生成全局配置
│   └── requirements.txt      # Python 依赖包列表
├── assets/              # 资源配置文件
│   └── Init/
│       └── Config/      # 生成的 TypeScript 配置文件
│           ├── ConfigData.ts   # 配置数据
│           ├── ConfigType.ts   # 配置类型定义
│           └── GlobalConfig.ts # 全局配置
└── README.md            # 项目说明文档
```

## 使用方法

### 使用 Python 源码运行
1. 安装依赖：`pip install -r script/requirements.txt`
2. 运行主程序：需要创建主入口脚本（如 run_all.py）来协调执行各个转换脚本

### 构建可执行程序（可选）
如需生成 EXE 可执行文件，运行：`python script/build_exe.py`

## 注意事项
- 需要在项目根目录创建 routePath.txt 文件，用于指定转表地址
- 确保 assets 文件夹存在于项目目录中
- 生成的 TypeScript 文件将输出到 `assets/Init/Config/` 目录
