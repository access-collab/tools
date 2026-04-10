import csv
import json
import re
import sys
from pathlib import Path

special_sheets = ["OPERATIONS_RE_FORM", "MAIN_RE_FORM"]


def read_data(data: list[str]):
    pass


def write_mappings(data_root_folder: Path, vlopse_name: str, data):
    mapping_path = data_root_folder / "vlopses" / f"{vlopse_name.lower()}.json"
    with open(mapping_path) as f:
        config = json.load(f)
    mapping = config["mappings"]
    conditions = config["conditions"]
    for row in data:
        id = row["id"]
        if id in mapping:
            # already defined
            continue
        src = row["MAIN_Question"]
        operation = row["Operation"]
        required = row["Required"]
        condition = row["Condition"]
        has_op = len(operation)
        has_condition = condition is not None and len(condition)
        if ", " in src:
            src = src.split(", ")
        if not has_op and not has_condition:
            # simple mapping
            mapping[id] = src
        elif has_op:
            # "M14": { "src": "org-addr-country", "operation": "make-iso" },
            mapping[id] = {"src": src, "operation": operation}
        elif isinstance(src, list):
            print("multi srcs should have an operator!")
            print(src)
            print(operation)

        elif has_condition:
            if src in conditions:
                # already defined
                continue
            match = re.findall(
                r"([A-Z]\d+)\s*==\s*(.*?)(?=\s+(?:AND|&&)\s+[A-Z]\d+\s*==|$)", condition
            )
            conds = []
            for cond_id, eq_val in match:
                condition = {"question_id": cond_id, "operator": "eq", "value": eq_val}
                conds.append(condition)
            if not len(conds):
                print(f"Unable to parse condition {condition} in {id}")
                continue
            conditions[src] = conds
        else:
            print("UNSPPORTED?")
            print(f"{id=}, {src=}, {operation=}, {required=}, {condition=}")

    with open(mapping_path, "w") as f:
        config["mappings"] = mapping
        config["conditions"] = conditions
        json.dump(config, f, indent=2)
    # print(f"===={vlopse_name}====")
    # print(mapping)
    # print(conditions)


def export_tables(data_root_folder: Path, vlopse_name: str, prefix: list[str], data):
    data_path = data_root_folder / "questions" / f"{vlopse_name}.json"
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
            if vlopse_name not in ["Meta", "TikTok"]:
                # FIXME: Dev mode
                continue

            prefix, table = partition_prefix(tsv)

            data = list(csv.DictReader(table, delimiter="\t"))
            export_tables(export_path, vlopse_name, prefix, data)
            write_mappings(export_path, vlopse_name, data)
