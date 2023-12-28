import processFile as pf
import sys
import task_1 as t1

"""
Argument Syntax: python task_3.py house-prices.csv --method=<method>  --columns <col1> <col2> <col3> ... --out=<output file name>
Note: 
    - task_3.py: chương trình thực thi nhiệm vụ "Fill in the missing value using mean, median (for numeric properties) and mode (for the categorical attribute)."
    - house-prices.csv: tệp dữ liệu đầu vào.
    - --method: phương pháp áp dụng xử lý bài toán.
        + mean: trung bình. (dành cho thuộc tính số)
        + median: trung vị. (dành cho thuộc tính số)
        + mode: giá trị có tần số xuất hiện nhiều nhất (dành cho thuộc tính định dang, phân loại)
    - --columns: các cột thuộc tính thiếu dữ liệu cần thêm vào.
    - --out: tệp dữ liệu đầu ra. (để lưu dữ liệu mới)
"""


def numeric_attributes(dataset: list[dict], columns: set) -> set:
    """
    Trả về một tập hợp các thuộc tính numerical bị thiếu dữ liệu.

    Args:
        dataset (list of dict): Các dòng dữ liệu được lưu trữ dưới dạng list.
        columns (set): Tập hợp các dòng bị thiếu dữ liệu.

    Returns:
        set: Tập hợp thuộc tính Numeric.
    """

    return {
        column
        for column in columns
        if all(row.get(column, "") == "" for row in dataset) or any(row.get(column, "").replace(".", "").isnumeric() for row in dataset)
    }


def fill_mean(dataset: list[dict], columns: list[str]) -> list[dict]:
    """
    Điền các dòng bị thiếu dữ liệu bằng giá trị trung bình của các cột tương ứng.

    Args:
        dataset (list of dict): Các dòng dữ liệu được lưu trữ dưới dạng list.
        columns (list of str): Tập hợp các dòng cần thêm dữ liệu.

    Returns:
        Bộ dữ liệu đã được thêm giá trị.
    """

    # Calculate the mean for each column
    list_mean, mean = {column: []
                       for column in columns}, {column: 0 for column in columns}

    for row in dataset:
        for column in columns:
            value = row[column]
            if value != "" and value is not None:
                list_mean[column].append(
                    float(value) if "." in value else int(value))

    for column, values in list_mean.items():
        if values:
            mean[column] = sum(values) / len(values)

    for row in dataset:
        for column in columns:
            if row[column] == "" or row[column] is None:
                row[column] = mean[column]

    return dataset


def fill_median(dataset: list[dict], columns: list[str]) -> list[dict]:
    """
    Điền các dòng bị thiếu dữ liệu bằng giá trị trung vị của các cột tương ứng.

    Args:
        dataset (list of dict): Các dòng dữ liệu được lưu trữ dưới dạng list.
        columns (list of str): Tập hợp các dòng cần thêm dữ liệu.

    Returns:
        Bộ dữ liệu đã được thêm giá trị.
    """

    # Calculate the median for each column
    list_median, median = {column: []
                           for column in columns}, {column: 0 for column in columns}

    for row in dataset:
        for column in columns:
            value = row[column]
            if value != "" and value is not None:
                list_median[column].append(
                    float(value) if "." in value else int(value))

    for column in columns:
        values = list_median[column]
        values.sort()
        if values:
            median_index = len(values) // 2
            median[column] = values[median_index]

    for row in dataset:
        for column in columns:
            if row[column] == "" or row[column] is None:
                row[column] = median[column]

    return dataset


def fill_mode(dataset: list[dict], columns: list[str]) -> list[dict]:
    """
    Điền các dòng bị thiếu dữ liệu bằng giá trị Mode của các cột tương ứng.

    Args:
        dataset (list of dict): Các dòng dữ liệu được lưu trữ dưới dạng list.
        columns (list of str): Tập hợp các dòng cần thêm dữ liệu.

    Returns:
        Bộ dữ liệu đã được thêm giá trị.
    """

    # Calculate the mode for each column
    list_mode, mode = {column: {}
                       for column in columns}, {column: "None" for column in columns}

    for row in dataset:
        for column in columns:
            value = row[column]
            if value != "" and value is not None:
                if value in list_mode[column]:
                    list_mode[column][value] += 1
                else:
                    list_mode[column][value] = 1

    for column in columns:
        most_common_value = ""
        max_occurrences = 0
        for value, occurrences in list_mode[column].items():
            if occurrences > max_occurrences:
                most_common_value = value
                max_occurrences = occurrences
        mode[column] = most_common_value

    for row in dataset:
        for column in columns:
            if row[column] == "" or row[column] is None:
                row[column] = mode[column]

    return dataset


def fill_data(dataset: list[dict], method: str, columns: list[str], outputFile: str) -> None:
    """
    Thêm vào các dữ liệu còn thiếu tùy vào phương pháp và cột tương ứng.

    Args:
        dataset (list of dict): Các dòng dữ liệu được lưu trữ dưới dạng list.
        method (str): Phương pháp truyền vào (mean, mode, median).
        columns (list of str): Tập hợp các cột dữ liệu thiếu được truyền vào.
        outputFile (str): Tên tệp Output.

    """
    missingColumns = t1.extract_columns_with_missing_values(dataset)
    missingColumnsName = set(column[0] for column in missingColumns)
    numericColumns = numeric_attributes(dataset, missingColumnsName)
    filling_functions = {
        "mean": fill_mean,
        "mode": fill_mode,
        "median": fill_median
    }

    # Check Method hợp lệ không
    if method not in filling_functions:
        raise ValueError(
            "Invalid method. Choose from 'mean', 'mode', or 'median'.")
    fill_function = filling_functions[method]
    for column in columns:
        if column in numericColumns:
            # Thuộc tính Numerical thì dùng Mode
            if method in ["mean", "median"]:
                dataset = fill_function(dataset, [column])
            else:
                raise ValueError(
                    f"Method '{method}' cannot be used on a numeric column: {column}")
        else:
            # Thuộc tính Categorical thì dùng Mode
            if method == "mode":
                dataset = fill_function(dataset, [column])
            else:
                raise ValueError(
                    f"Method '{method}' cannot be used on a categorical column: {column}")

    pf.write_csv_data(dataset, outputFile)


if __name__ == '__main__':
    if len(sys.argv) <= 5:
        print(
            "Usage: python task_3.py house-prices.csv --method=<operation> --columns <col1> <col2> ... --out=<output file name>")
        sys.exit(1)
    if sys.argv[2].split("=")[0] != "--method" or sys.argv[3] != "--columns" or sys.argv[-1].split("=")[0] != "--out":
        print("Invalid command-line arguments. Use --method, --columns and --out.")
        sys.exit(1)

    # Đọc dữ liệu từ tệp CSV
    data = pf.read_csv_file(sys.argv[1])

    # Điền vào giá trị thiếu và ghi dữ liệu mới vào tệp CSV mới
    fill_data(data, sys.argv[2].split("=")[1],
              sys.argv[4:-1], sys.argv[-1].split("=")[1])
