import os

def ensure_path_exists(file_path):
    dir_path = os.path.dirname(file_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # 自动创建空文件（如果需要）
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            pass

def generate_global_config(type_path, data_path, output_path):
    # 获取所有数据对象名
    ensure_path_exists(data_path)

    with open(data_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    data_vars = [line.split()[2] for line in lines if line.startswith("export const")]

    # 获取所有接口名
    ensure_path_exists(type_path)

    with open(type_path, "r", encoding="utf-8") as f:
        type_lines = f.readlines()
    type_map = {}
    for line in type_lines:
        if line.startswith("export interface"):
            interface = line.split()[2]
            name = interface.replace("Info", "")
            type_map[name + "Data"] = interface

    ensure_path_exists(output_path)
    # 生成 GlobalConfig.ts
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("// 自动生成，请勿手动修改\n")
        f.write('import {\n')
        for interface in type_map.values():
            f.write(f"  {interface},\n")
        f.write('} from "./ConfigType";\n')
        f.write('import {\n')
        for var in data_vars:
            f.write(f"  {var},\n")
        f.write('} from "./ConfigData";\n\n')
        f.write("export const GlobalConfig: {\n")
        for var in data_vars:
            f.write(f"  {var.replace('Data','')}: {type_map.get(var, 'any')}[],\n")
        f.write("} = {\n")
        for var in data_vars:
            f.write(f"  {var.replace('Data','')}: {var} as {type_map.get(var, 'any')}[],\n")
        f.write("};\n")
        # 新增全局方法
        f.write("""
/**
 * 根据表名和id获取属性对象
 * @param table 表名（如 'XXX'）
 * @param id 主键id
 */
export function getConfigById(table: keyof typeof GlobalConfig, id: number | string) {
  const arr = GlobalConfig[table];
  if (!Array.isArray(arr)) return undefined;
  return arr.find(item => item.id === id);
}
""")
        # 为每个表生成单独的 getXXXById 方法
        for var in data_vars:
            table_name = var.replace('Data', '')
            interface = type_map.get(var, 'any')
            f.write(f"""
/**
 * 获取 {table_name} 表中指定 id 的数据
 * @param id 主键id
 */
export function get{table_name.capitalize()}ById(id: number | string): {interface} | undefined {{
  const arr = GlobalConfig.{table_name};
  if (!Array.isArray(arr)) return undefined;
  return arr.find(item => item.id === id);
}}
""")

def load_paths(config_file="./routePath.txt"):
    paths = {
        "INPUT_PATH": "./",
        "OUTPUT_TS_PATH": "../assets/Init/Config/ConfigType.ts",
        "OUTPUT_DATA_PATH": "../assets/Init/Config/ConfigData.ts",
        "GLOBAL_CONFIG_PATH": "../assets/Init/Config/GlobalConfig.ts"
    }
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    paths[key.strip()] = value.strip()
    return paths

def main():
    paths = load_paths()
    type_path = paths["OUTPUT_TS_PATH"]
    data_path = paths["OUTPUT_DATA_PATH"]
    output_path = paths["GLOBAL_CONFIG_PATH"]
    generate_global_config(type_path, data_path, output_path)


if __name__ == "__main__":
    main()