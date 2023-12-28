import csv
from pathlib import Path
from typing import List, Dict


def read_csv_file(input_file: str) -> List[Dict[str, str]]:
    """
    Đọc dữ liệu từ tệp CSV.

    Args:
        input_file (str): Đường dẫn đến tệp CSV cần đọc.

    Returns:
        data_list (list): Danh sách các từ điển chứa dữ liệu từ tệp CSV.
    """
    if not Path(input_file).exists():
        raise FileNotFoundError(
            f"File not found.",
        )

    with open(input_file, mode='r', encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)

        data_list = [row for row in csv_reader]

    return data_list


def write_csv_data(data: List[Dict[str, str]], output_file: str) -> None:
    """
    Ghi dữ liệu vào tệp CSV.

    Args:
        data (list of dict): Danh sách các từ điển chứa dữ liệu từ tệp CSV gốc.
        output_file (str): Đường dẫn đến tệp CSV cần ghi.
    """

    with open(output_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys(), delimiter=",")
        writer.writeheader()
        writer.writerows(data)
