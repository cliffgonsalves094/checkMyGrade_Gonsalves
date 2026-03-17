import csv
import os
from typing import Iterable


def save_to_csv(filename, data_list):

    unique_keys = getattr(data_list[0], "UNIQUE_KEYS", []) if data_list else []
    for key in unique_keys:
        seen = set()
        for item in data_list:
            value = getattr(item, key, None)
            if value in seen:
                print(
                    f"Error: duplicate {key} found ({value}). Not saving."
                )
                return False
            seen.add(value)

    with open(filename, "w", newline="") as f:

        writer = csv.writer(f)

        if data_list:
            header = getattr(data_list[0], "CSV_HEADERS", None)
            if header:
                writer.writerow(header)

        for item in data_list:
            writer.writerow(item.to_list())
    return True


def append_to_csv(filename, row, headers=None):
    needs_header = not os.path.exists(filename) or os.path.getsize(filename) == 0

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if needs_header and headers:
            writer.writerow(headers)
        writer.writerow(row)


def load_from_csv(filename, cls):

    objects = []

    try:

        with open(filename, "r") as f:

            reader = csv.reader(f)

            first_row = next(reader, None)

            if first_row:
                header = getattr(cls, "CSV_HEADERS", None)
                if header and first_row != list(header):
                    obj = cls(*first_row)
                    objects.append(obj)

            for row in reader:
                obj = cls(*row)
                objects.append(obj)

    except FileNotFoundError:
        pass

    return objects
