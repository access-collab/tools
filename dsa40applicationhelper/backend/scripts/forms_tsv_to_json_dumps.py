import csv
import json
import re
import sys
from pathlib import Path

special_sheets = ["OPERATIONS_RE_FORM", "MAIN_RE_FORM"]


def read_data(data: list[str]):
    pass


def export(data_root_folder: Path, vlopse_name: str, prefix: list[str], data):
    data_path = data_root_folder / "questions" / f"{ vlopse_name }.json"
    prefix_path = data_root_folder / "vlopses" / f"{vlopse_name}_meta.txt"
    data_path.parent.mkdir(exist_ok=True)
    with open(data_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"{data_path}")
    prefix_path.parent.mkdir(exist_ok=True)
    with open(prefix_path, "w") as f:
        f.writelines(prefix)
    print(f"{prefix_path}")


def partition_prefix(path: Path):
    prefix: list[str] = []
    table: list[str] = []
    column_header = None
    with open(path) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith("id"):
                column_header = line
                continue
            if column_header:
                table.append(line)
            else:
                prefix.append(line)
    if not column_header:
        raise TypeError(f"Couldn't find column header in {path}")
    table.insert(0, column_header)
    return prefix, table


if __name__ == "__main__":
    data_path = sys.argv[1]
    data_path = Path(data_path)
    export_path = sys.argv[2]
    export_path = Path(export_path)
    for tsv in data_path.glob("*.tsv"):
        match = re.match(r".* - (.*)", tsv.stem)
        if match:
            vlopse_name = match.group(1)
            if vlopse_name in special_sheets:
                print(f"Skipping {vlopse_name}")
                continue

            prefix, table = partition_prefix(tsv)

            data = list( csv.DictReader(table, delimiter="\t") )
            export(export_path, vlopse_name, prefix, data)
