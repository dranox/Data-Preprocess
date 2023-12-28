import sys
import processFile as pf

"""
Argument Syntax: python task_1.py house-prices.csv
Note: 
    - task_1.py: chương trình thực thi nhiệm vụ "Extract columns with missing values."
    - house-prices.csv: tệp dữ liệu đầu vào.
"""


def extract_columns_with_missing_values(dataset: list) -> list:
    """
    Liệt kê các cột bị thiếu dữ liệu.
    Args:
        dataset (list): Các dòng dữ liệu được lưu trữ dưới dạng list.

    Returns:
        missing_columns (list): List chứa thông tin về các cột bị thiếu dữ liệu.
    """
    return [(col, sum(1 for row in dataset if row[col] == ''))
            for col in dataset[0].keys() if any(row[col] == '' for row in dataset)]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(
            "Usage: python task_1.py house-prices.csv")
        sys.exit(1)
    # Đọc dữ liệu từ tệp CSV
    data = pf.read_csv_file((sys.argv[1]))

    # Trích xuất thuộc tính thiếu dữ liệu
    missingColumns = extract_columns_with_missing_values(data)

    # In ra console các thuộc tính bị thiếu dữ liệu
    print(f"Dataset have {len(missingColumns)} missing columns.")
    for column_name, value in missingColumns:
        print(f"Column: {column_name}, Missing Values: {value}")
