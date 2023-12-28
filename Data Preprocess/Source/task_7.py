from typing import List, Dict
import processFile as pf
import sys

"""
Argument Syntax: python task_7.py house-prices.csv --method=<operation> --columns <col1> <col2> ... --out=<output file name>
Note: 
    - task_7.py: chương trình thực thi nhiệm vụ "Normalize a numeric attribute using min-max and Z-score methods."
    - house-prices.csv: tệp dữ liệu đầu vào.
    - --method: phương pháp áp dụng xử lý bài toán.
        + minmax.
        + zscore.
    - --columns: các cột thuộc tính số cần thực hiện bài toán.
    - --out: tệp dữ liệu đầu ra. (để lưu dữ liệu mới)
"""


def is_numeric_column(data_list: List[Dict[str, str]], column_name: str) -> list:
    """
    Kiểm tra xem một cột trong danh sách có phải là số hay không.

    Args:
        data_list (list of dict): Danh sách các từ điển chứa dữ liệu từ tệp CSV gốc.
        column_name (str): Tên của cột cần kiểm tra.

    Returns:
        List các thuộc tính Numeric.
    """
    return {
        column
        for column in column_name
        if all(row.get(column, "") == "" for row in data_list) or any(row.get(column, "").replace(".", "").isnumeric() for row in data_list)
    }


def normalize(data_list: List[Dict[str, str]], method: str, columns: List[str]) -> None:
    """
    Chuẩn hóa dữ liệu trong các cột đã cho.

    Args:
        data_list (list of dict): Danh sách các từ điển chứa dữ liệu từ tệp CSV gốc.
        method (str): Phương pháp chuẩn hóa, có thể là "minmax" hoặc "zscore".
        columns (list of str): Danh sách các tên cột cần chuẩn hóa.
    """
    numericColumns = is_numeric_column(data_list, list(data_list[0].keys()))
    for column_name in columns:
        if column_name in numericColumns:
            column_data = [float(row[column_name])
                           for row in data_list if row[column_name] != ""]

            if method == "minmax":
                min_val = min(column_data)
                max_val = max(column_data)
                for row in data_list:
                    if row[column_name] != "":
                        row[column_name] = (
                            float(row[column_name]) - min_val) / (max_val - min_val)

            elif method == "zscore":
                mean_val = sum(column_data) / len(column_data)
                std_dev_val = (
                    sum((x - mean_val) ** 2 for x in column_data) / len(column_data)) ** 0.5
                for row in data_list:
                    if row[column_name] != "":
                        row[column_name] = (
                            float(row[column_name]) - mean_val) / std_dev_val

            else:
                print(f"Invalid method: {method}.")
        else:
            print(f"{column_name} is not numeric, so it can't be standardized.")


if __name__ == '__main__':

    if len(sys.argv) <= 5:
        print(
            "Usage: python task_7.py house-prices.csv --method=<operation> --columns <col1> <col2> ... --out=<output file name>")
        sys.exit(1)
    if sys.argv[2].split("=")[0] != "--method" or sys.argv[3] != "--columns" or sys.argv[-1].split("=")[0] != "--out":
        print("Invalid command-line arguments. Use --method, --columns and --out.")
        sys.exit(1)
    # Đọc dữ liệu từ tệp CSV
    data = pf.read_csv_file(sys.argv[1])

    # Chuẩn hóa dữ liệu
    normalize(data, sys.argv[2].split("=")[1], sys.argv[4:-1])

    # Ghi dữ liệu mới vào tệp CSV mới
    pf.write_csv_data(data, sys.argv[-1].split("=")[1])
