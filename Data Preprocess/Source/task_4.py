from typing import List, Dict
import processFile as pf
import sys
import task_2 as t2
"""
Argument Syntax: python task_4.py house-prices.csv --threshold=<value in [0,1]> --out=<output file name>
Note: 
    - task_4.py: chương trình thực thi nhiệm vụ "Deleting rows containing more than a particular number of missing values (Example: delete rows with the number of missing values is more than 50% of the number of attributes)."
    - house-prices.csv: tệp dữ liệu đầu vào.
    - --threshold: Tỷ lệ (ngưỡng) để xóa giá trị. (BẮT BUỘC NẰM TRONG KHOẢNG [0,1])
    - --out: tệp dữ liệu đầu ra. (để lưu dữ liệu mới)
"""


def remove_rows_with_missing_values(data: List[Dict[str, str]], threshold: float) -> List[Dict[str, str]]:
    """
    Loại bỏ các hàng có giá trị bị thiếu từ dữ liệu.

    Args:
        data (list of dict): Danh sách các từ điển chứa dữ liệu từ tệp CSV gốc.
        threshold (float): Ngưỡng để xác định số lượng giá trị bị thiếu tối đa cho một hàng.

    Returns:
        data (list of dict): Danh sách các từ điển sau khi đã loại bỏ các hàng có giá trị bị thiếu.
    """
    num_attributes = len(data[0])
    rows_to_delete = []

    for i in range(len(data)):
        row = data[i]
        num_missing_values = list(row.values()).count('')
        if num_missing_values > num_attributes * threshold:
            rows_to_delete.append(i)

    for i in sorted(rows_to_delete, reverse=True):
        del data[i]

    return data


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(
            "Usage: python task_4.py house-prices.csv --threshold=<value in [0,1]> --out=<output file name>")
        sys.exit(1)
    if sys.argv[2].split("=")[0] != "--threshold" or float(sys.argv[2].split("=")[1]) < 0 or float(sys.argv[2].split("=")[1]) > 1 or sys.argv[-1].split("=")[0] != "--out":
        print(
            "Invalid command-line arguments. Use --threshold, --out and required threshold is in the range [0,1].")
        sys.exit(1)

    # Đọc dữ liệu từ tệp CSV
    data = pf.read_csv_file(sys.argv[1])

    # Xóa dòng thiếu dữ liệu theo threshold
    cleaned_data = remove_rows_with_missing_values(
        data, float(sys.argv[2].split("=")[1]))

    # Đếm số dòng thiếu dữ liệu
    missingLines = t2.count_lines_with_missing_data(cleaned_data)

    # In ra màn hình số dòng thiếu dữ liệu
    print(f"The number of lines with missing data: {missingLines}")

    # Ghi dữ liệu mới vào tệp CSV mới
    pf.write_csv_data(cleaned_data, sys.argv[-1].split("=")[-1])
