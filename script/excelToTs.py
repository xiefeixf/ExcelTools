import json
import re
import pandas as pd
import os

def ensure_path_exists(file_path):
    dir_path = os.path.dirname(file_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # 自动创建空文件（如果需要）
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            pass


def generate_ts_interface(sheet_name , excel_file_name, data_frame):
    """
    根据DataFrame生成TypeScript接口定义
    """
    interface_name = excel_file_name.replace("(", "").replace(")", "").rsplit('.', 1)[0] + "Info"
    ts_lines = [f"export interface {interface_name} {{"]

    xyz_indices = {}
    for col_index, column in enumerate(data_frame.columns):
        field_name = data_frame.iloc[0, col_index]
        if pd.isna(field_name):
            continue
        if field_name in ["x", "y", "z"]:
            xyz_indices[field_name] = col_index
            continue  # 暂时跳过 x,y,z 字段
        field_type = data_frame.iloc[1, col_index]
        if field_type == "number":
            ts_type = "number"
        elif field_type == "float":
            ts_type = "number"
        elif field_type == "string":
            ts_type = "string"
        elif field_type == "boolean":
            ts_type = "boolean"
        elif field_type == "bool":
            ts_type = "boolean"
        elif field_type == "array":
            fourth_row = str(data_frame.iloc[3, col_index])
            ts_type = parse_array_type(fourth_row)
        elif field_type == "json":
            fourth_row = str(data_frame.iloc[3, col_index])
            ts_type = parse_json_type(fourth_row)
        else:
            ts_type = "any"
        field_comment = data_frame.iloc[2, col_index]
        ts_lines.append(f"  /** {field_comment} */")
        ts_lines.append(f"  {field_name}: {ts_type};")

    # 如果x,y,z都存在，则合并为pos字段
    if all(k in xyz_indices for k in ["x", "y", "z"]):
        ts_lines.append(f"  /** 位置坐标 */")
        ts_lines.append(f"  pos: {{ x: number, y: number, z: number }};")

    ts_lines.append("}")
    return "\n".join(ts_lines)

def parse_array_type(type_str):
    """
    解析如 [1,2,3] 或 ["a","b"] 为 number[] 或 string[] 或 any[]
    """
    if not type_str or type_str == 'nan':
        return "any[]"
    try:
        arr = json.loads(type_str)
    except Exception:
        try:
            arr = eval(type_str)
        except Exception:
            return "any[]"
    if isinstance(arr, list):
        if all(isinstance(x, (int, float)) for x in arr):
            return "number[]"
        elif all(isinstance(x, str) for x in arr):
            return "string[]"
        else:
            return "any[]"
    return "any[]"

def parse_json_type(type_str):
    """
    解析如 {"atk":100,"hp":999,"tek":[1,3,8]} 为 { atk: number, hp: number, tek: number[] }
    """
    if not type_str or type_str == 'nan':
        return "any"
    # 自动补全key的引号
    def add_quotes(s):
        return re.sub(r'([{,]\s*)(\w+)\s*:', r'\1"\2":', s)
    try:
        # 尝试标准json解析
        type_str_fixed = add_quotes(type_str)
        obj = json.loads(type_str_fixed)
    except Exception:
        return "any"
    fields = []
    for key, val in obj.items():
        if isinstance(val, int) or isinstance(val, float):
            ts_type = "number"
        elif isinstance(val, str):
            ts_type = "string"
        elif isinstance(val, list):
            # 判断列表元素类型
            if all(isinstance(x, (int, float)) for x in val):
                ts_type = "number[]"
            elif all(isinstance(x, str) for x in val):
                ts_type = "string[]"
            else:
                ts_type = "any[]"
        elif isinstance(val, dict):
            ts_type = "object"
        else:
            ts_type = "any"
        fields.append(f"{key}: {ts_type}")
    return "{ " + ", ".join(fields) + " }"

def folder_to_ts(folder_path, output_ts_file):
    """
    将文件夹中的所有Excel文件转换为一个TypeScript文件
    """
    ensure_path_exists(output_ts_file)

    with open(output_ts_file, "w", encoding="utf-8") as ts_file:
        for file_name in os.listdir(folder_path):
            if file_name.startswith("~$"):
                continue  # 跳过Excel临时文件
            if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
                excel_path = os.path.join(folder_path, file_name)

                # 读取Excel文件
                excel_data = pd.ExcelFile(excel_path)

                for sheet_name in excel_data.sheet_names:
                    # 读取每个工作表的数据
                    df = excel_data.parse(sheet_name, header=None)
                    if df.empty:
                        continue

                    # 生成TypeScript接口
                    ts_interface = generate_ts_interface(sheet_name ,file_name , df)

                    # 写入文件
                    ts_file.write(ts_interface + "\n\n")

    print(f"TypeScript definitions have been written to {output_ts_file}")

## 读取配置文件获取路径
def load_paths(config_file="./routePath.txt"):
    paths = {
        "INPUT_PATH": "./",
        "OUTPUT_TS_PATH": "../assets/Init/Config/ConfigType.ts"
    }
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    if key.strip() in paths:
                        paths[key.strip()] = value.strip()
    return paths["INPUT_PATH"], paths["OUTPUT_TS_PATH"]

def main():
    # 路径从配置文件读取
    folder_path, output_file_path = load_paths()
    # 路径不存在 自动创建输出文件夹
    output_dir = os.path.dirname(output_file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if not os.path.exists(folder_path):
        print(f"Error: The folder {folder_path} does not exist.")
    else:
        folder_to_ts(folder_path, output_file_path)

if __name__ == "__main__":
    main()