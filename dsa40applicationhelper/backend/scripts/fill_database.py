import sys
from json import load
from pathlib import Path

import requests

vlopse_name = sys.argv[1]
vlopse_path = sys.argv[2]

json_qs = Path(vlopse_path)
BASE_URL = "http://localhost:8000"
URL = f"{BASE_URL}/api/vlopse/{vlopse_name}/question"


def build_request_data(q: dict):
    req_data = {
        "id": q["id"],
        "text": q["Question"],
        "required": q["Required"],
        "details": q["Details"],
    }
    i_type = None
    match q["Type"]:
        case "free form":
            # class Text(BaseModel):
            #     i_type: Literal["text"]
            #     max_length: int | None = None
            req_data["input_type"] = "text"
        case "selection":
            # class Selection(BaseModel):
            #     i_type: Literal["selection"]
            #     options: list[str]
            opts = q["Options"]
            opts = opts.split(", ")
            if len(opts) <= 1:
                opts = opts[0].split("; ")
            if len(opts) <= 1:
                print(opts)
                raise TypeError("selections should have more than 1 value!")
            req_data["input_type"] = "selection"
            i_type = {"type": "selection", "options": opts}
        case "file upload":
            req_data["input_type"] = "file_upload"

        case "multi-select" | "date-select":
            raise NotImplementedError(f"{q['Type']} not yet implemented!")

    # {
    #   "id": "T1",
    #   "text": "Your name as shown on your professional profile (e.g. your university or research organisation profile",
    #   "required": "true",
    #   "input_type": {
    #     "i_type": "text"
    #   }
    # },
    req_data["config"] = i_type
    return req_data


#
#
#
# class Boolean(BaseModel):
#     i_type: Literal["boolean"]
#
#
#
# class DateRange(BaseModel):
#     i_type: Literal["daterange"]
#     begin: Literal["TODO"]
#

# service = QuestionService(None)
with open(json_qs) as f:
    qs = load(f)
    print(f"Found {len(qs)} questions, adding them..")
    for i, q in enumerate(qs):
        try:
            req_data = build_request_data(q)
        except Exception as e:
            print(f"{q['id']} caused {e}")
            continue
        res = requests.post(URL, json=req_data, timeout=5)
        if res.status_code != 200:
            if res.status_code == 422:
                print(f"[ERR]: {res.json()}")
                break
            if res.status_code == 409:
                continue
            print(res.status_code)
            print(res.text)
