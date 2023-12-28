import processFile as pf
import sys

"""
Argument Syntax: python task_2.py house-prices.csv
Note: 
    - task_2.py: chương trình thực thi nhiệm vụ "Count the number of lines with missing data."
    - house-prices.csv: tệp dữ liệu đầu vào.
"""


def count_lines_with_missing_data(dataset: list) -> int:
    """Đếm số lượng dòng bị thiếu dữ liệu.
    Args:
        dataset (list): các dòng dữ liệu được lưu trữ dưới dạng list

    Returns:
        Số lượng dòng bị thiếu.
    """
    return sum(1 for row in dataset if any(value == '' for value in row.values()))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(
            "Usage: python task_2.py house-prices.csv")
        sys.exit(1)

    # Đọc dữ liệu từ tệp CSV
    data = pf.read_csv_file((sys.argv[1]))

    #Đếm số dòng thiếu dữ liệu
    missingLines = count_lines_with_missing_data(data)

    #In ra màn hình số dòng thiếu dữ liệu
    print(f"The number of lines with missing data: {missingLines}")
