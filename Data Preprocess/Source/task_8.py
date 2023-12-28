import sys
import processFile as pf

"""
Argument Syntax: python task_8.py house-prices.csv --method=<operation> --columns <col1> <col2> --out=<output file name>
Note: 
    - task_8.py: chương trình thực thi nhiệm vụ "Performing addition, subtraction, multiplication, and division between two numerical attributes."
    - house-prices.csv: tệp dữ liệu đầu vào.
    - --method: phương pháp áp dụng xử lý bài toán.
        + add or +: phép cộng.
        + sub or -: phép trừ.
        + mul or *: phép nhân.
        + div or /: phép chia.
    - --columns: 2 cột thuộc tính số cần thực hiện bài toán.
    - --out: tệp dữ liệu đầu ra. (để lưu dữ liệu mới)
"""


def perform_operation(list1: list, list2: list, operator: str) -> list:
    if operator not in ('+', '-', '*', '/', 'add', 'sub', 'mul', 'div'):
        raise ValueError(
            "Invalid operator. Use '+', '-', '*', '/' or 'add', 'sub', 'mul', 'div'.")

    if len(list1) != len(list2):
        raise ValueError("Input lists must have the same length.")

    result = []
    for v1, v2 in zip(list1, list2):
        try:
            v1, v2 = float(v1), float(v2)
            if operator == '+' or operator == 'add':
                result.append(v1 + v2)
            elif operator == '-' or operator == 'sub':
                result.append(v1 - v2)
            elif operator == '*' or operator == 'mul':
                result.append(v1 * v2)
            elif operator == '/' or operator == 'div':
                if v2 == 0:
                    result.append(float('inf'))  # Handle division by zero
                else:
                    result.append(v1 / v2)
        except (ValueError, TypeError):
            result.append(float('nan'))  # Handle categorical or empty values

    return result


def calculate_numerical_columns(dataset: list[dict], columns: list[str], function: str) -> list:
    column1 = [row.get(columns[0]) for row in dataset]
    column2 = [row.get(columns[1]) for row in dataset]

    result = perform_operation(column1, column2, function)

    return result


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print(
            "Usage: python task_8.py house-prices.csv --method=<operation> --columns <col1> <col2> --out=<output file name>")
        sys.exit(1)

    if sys.argv[2].split("=")[0] != "--method" or sys.argv[3] != "--columns" or sys.argv[-1].split("=")[0] != "--out":
        print("Invalid command-line arguments. Use --method, --columns and --out.")
        sys.exit(1)

    # Đọc dữ liệu từ tệp CSV
    data = pf.read_csv_file(sys.argv[1])

    # Thực hiện phép tính giữa 2 thuộc tính số
    result = calculate_numerical_columns(
        data,
        columns=(sys.argv[-3], sys.argv[-2]),
        function=sys.argv[2].split("=")[-1]
    )

    # lưu kết quả vào 1 cột mới tên là result
    data_with_result = [{**data[i], 'result': result[i]}
                        for i in range(len(data))]

    # Ghi dữ liệu mới vào tệp CSV mới
    pf.write_csv_data(data_with_result, sys.argv[-1].split("=")[-1])
