from typing import List, Dict
import processFile as pf
import sys
import task_2 as t2

"""
Argument Syntax: python task_6.py house-prices.csv --out=<output file name>
Note: 
    - task_6.py: chương trình thực thi nhiệm vụ "Delete duplicate samples."
    - house-prices.csv: tệp dữ liệu đầu vào.
    - --out: tệp dữ liệu đầu ra. (để lưu dữ liệu mới)
"""


def remove_duplicate_rows(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Loại bỏ các hàng trùng lặp từ dữ liệu.

    Args:
        data (list of dict): Danh sách các từ điển chứa dữ liệu từ tệp CSV gốc.

    Returns:
        unique_data (list of dict): Danh sách các từ điển sau khi đã loại bỏ các hàng trùng lặp.
    """
    # unique_data = list(dict(s) for s in set(tuple(d.items()) for d in data))

    # Tạo một tập hợp để loại bỏ các hàng trùng lặp
    set_of_tuples = set()

    # Duyệt qua từng hàng trong dữ liệu
    for d in data:
        # Chuyển đổi từ điển thành tuple và thêm vào tập hợp
        tuple_of_items = tuple(d.items())
        set_of_tuples.add(tuple_of_items)

    # Tạo một danh sách mới từ tập hợp các tuple
    list_of_dicts = []

    # Duyệt qua từng tuple trong tập hợp
    for s in set_of_tuples:
        # Chuyển đổi tuple thành từ điển và thêm vào danh sách
        dict_from_tuple = dict(s)
        list_of_dicts.append(dict_from_tuple)

    unique_data = list_of_dicts

    return unique_data


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(
            "Usage: python task_6.py house-prices.csv --out=<output file name>")
        sys.exit(1)

    if sys.argv[-1].split("=")[0] != "--out":
        print("Invalid command-line arguments. Use --out.")
        sys.exit(1)

    # Đọc dữ liệu từ tệp CSV
    data = pf.read_csv_file(sys.argv[1])

    # Xóa các dòng trùng lặp
    unique_data = remove_duplicate_rows(data)

    # Đếm số dòng thiếu dữ liệu
    missingLines = t2.count_lines_with_missing_data(unique_data)

    # In ra màn hình số dòng thiếu dữ liệu
    print(f"The number of lines with missing data: {missingLines}")

    # Ghi dữ liệu mới vào tệp CSV mới
    pf.write_csv_data(unique_data, sys.argv[-1].split("=")[-1])
