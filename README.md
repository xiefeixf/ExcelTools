# ExcelTools 使用说明

## 目录结构
```
ExcelTools_v2.1/
├── script/              # Python 源代码
│   ├── excelToTs.py          # Excel 转 TypeScript 接口定义
│   ├── excelToTsData.py      # Excel 转 TypeScript 数据
│   ├── generateGlobalConfig.py # 生成全局配置
│   ├── run_all.py            # 主程序入口
│   └── verify.py             # 验证工具
├── assets/              # 资源配置文件
└── dist/                # 编译输出
    └── ExcelTools.exe   # 可执行程序
```

## 使用方法

### 方式一：直接运行 EXE
1. 打开 `dist` 文件夹
2. 双击运行 `ExcelTools.exe`

### 方式二：使用 Python 源码
1. 安装依赖：`pip install -r script/requirements.txt`
2. 运行主程序：`python script/run_all.py`

## 注意事项
- 将 routePath.txt 放在项目根目录，填写转表地址
- 确保 assets 文件夹与 exe 在同一目录下
