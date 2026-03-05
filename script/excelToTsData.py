import pandas as pd
import json
import os

def ensure_path_exists(file_path):
    dir_path = os.path.dirname(file_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # 自动创建空文件（如果需要）
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            pass


def excel_to_ts_object(excel_path, output_ts_file):
    excel_data = pd.ExcelFile(excel_path)
    for sheet_name in excel_data.sheet_names:
        df = excel_data.parse(sheet_name, header=None)
        if df.empty or df.shape[0] < 4:
            continue

        # 字段名在第1行，类型在第2行
        field_names = df.iloc[0].tolist()
        field_types = df.iloc[1].tolist()
        data_rows = df.iloc[3:].values.tolist()  # 第5行开始是数据

        ts_objects = []
        for row in data_rows:
            obj = {}
            xyz_values = {}
            for idx, value in enumerate(row):
                field = field_names[idx]
                ftype = field_types[idx]
                if pd.isna(field):
                    continue
                # 收集 x, y, z 字段
                if field in ["x", "y", "z"]:
                    xyz_values[field] = float(value) if not pd.isna(value) else None
                    continue  # 不单独输出 x,y,z 字段
                if ftype == "number" or ftype == "float":
                    obj[field] = float(value) if not pd.isna(value) else None
                elif ftype == "string":
                    obj[field] = str(value) if not pd.isna(value) else None
                elif ftype == "boolean" or ftype == "bool":
                    if pd.isna(value):
                        obj[field] = None
                    elif isinstance(value, bool):
                        obj[field] = value
                    elif isinstance(value, (int, float)):
                        obj[field] = bool(value)
                    else:
                        # 字符串转换：true/True/1 -> True, false/False/0 -> False
                        str_val = str(value).strip().lower()
                        if str_val in ["true", "1", "yes"]:
                            obj[field] = True
                        elif str_val in ["false", "0", "no"]:
                            obj[field] = False
                        else:
                            obj[field] = bool(value)
                elif ftype == "array":
                    try:
                        obj[field] = json.loads(value) if value else None
                    except Exception:
                        obj[field] = None
                elif ftype == "json":
                    try:
                        obj[field] = json.loads(value) if value else None
                    except Exception:
                        obj[field] = None
                else:
                    obj[field] = value if not pd.isna(value) else None
            # 如果xyz都有，合并为pos
            if all(k in xyz_values for k in ["x", "y", "z"]):
                obj["pos"] = {
                    "x": xyz_values["x"],
                    "y": xyz_values["y"],
                    "z": xyz_values["z"]
                }
            ts_objects.append(obj)

        # 生成TS对象字符串
        ts_var_name = os.path.splitext(os.path.basename(excel_path))[0] + "Data"
        ts_content = f"export const {ts_var_name} = {json.dumps(ts_objects, ensure_ascii=False, indent=2)};\n"

        ensure_path_exists(output_ts_file)

        # 写入文件（追加模式）
        with open(output_ts_file, "a", encoding="utf-8") as f:
            f.write(ts_content)

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
    input_path = paths["INPUT_PATH"]
    output_ts_path = paths["OUTPUT_DATA_PATH"]
    if not os.path.exists(input_path):
        print(f"Error: The folder {input_path} does not exist.")
        return
    open(output_ts_path, "w", encoding="utf-8").close()
    for file_name in os.listdir(input_path):
        if file_name.startswith("~$"):
            continue
        if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
            excel_path = os.path.join(input_path, file_name)
            excel_to_ts_object(excel_path, output_ts_path)
    print(f"TypeScript data objects have been written to {output_ts_path}")

if __name__ == "__main__":
    main()