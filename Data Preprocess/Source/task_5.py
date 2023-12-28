from typing import List, Dict
import processFile as pf
import sys
import task_1 as t1

"""
Argument Syntax: python task_5.py house-prices.csv --threshold=<value in [0,1]> --out=<output file name>
Note: 
    - task_5.py: chương trình thực thi nhiệm vụ "Deleting columns containing more than a particular number of missing values (Example: delete columns with the number of missing values is more than 50% of the number of samples)."
    - house-prices.csv: tệp dữ liệu đầu vào.
    - --threshold: Tỷ lệ (ngưỡng) để xóa giá trị. (BẮT BUỘC NẰM TRONG KHOẢNG [0,1])
    - --out: tệp dữ liệu đầu ra. (để lưu dữ liệu mới)
"""


def remove_columns_with_missing_values(data: List[Dict[str, str]], threshold: float) -> List[Dict[str, str]]:
    """
    Loại bỏ các cột có giá trị bị thiếu từ dữ liệu.

    Args:
        data (list of dict): Danh sách các từ điển chứa dữ liệu từ tệp CSV gốc.
        threshold (float): Ngưỡng để xác định số lượng giá trị bị thiếu tối đa cho một cột.

    Returns:
        data (list of dict): Danh sách các từ điển sau khi đã loại bỏ các cột có giá trị bị thiếu.
    """
    num_samples = len(data)
    columns_to_delete = []

    for key in data[0].keys():
        column_values = [row[key] for row in data]
        num_missing_values = column_values.count('')
        if num_missing_values > num_samples * threshold:
            columns_to_delete.append(key)

    for key in columns_to_delete:
        for row in data:
            del row[key]

    return data


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(
            "Usage: python task_5.py house-prices.csv --threshold=<value in [0,1]> --out=<output file name>")
        sys.exit(1)
    if sys.argv[2].split("=")[0] != "--threshold" or float(sys.argv[2].split("=")[1]) < 0 or float(sys.argv[2].split("=")[1]) > 1 or sys.argv[-1].split("=")[0] != "--out":
        print(
            "Invalid command-line arguments. Use --threshold, --out and required threshold is in the range [0,1].")
        sys.exit(1)

    # Đọc dữ liệu từ tệp CSV
    data = pf.read_csv_file(sys.argv[1])

    # Xóa cột thiếu dữ liệu theo threshold
    cleaned_data = remove_columns_with_missing_values(
        data, float(sys.argv[2].split("=")[1]))

    # Trích xuất thuộc tính thiếu dữ liệu
    missingColumns = t1.extract_columns_with_missing_values(cleaned_data)

    # In ra console các thuộc tính bị thiếu dữ liệu
    print(f"Dataset have {len(missingColumns)} missing columns.")
    for column_name, value in missingColumns:
        print(f"Column: {column_name}, Missing Values: {value}")

    # Ghi dữ liệu mới vào tệp CSV mới
    pf.write_csv_data(cleaned_data, sys.argv[-1].split("=")[-1])
