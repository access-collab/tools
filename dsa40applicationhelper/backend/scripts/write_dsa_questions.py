import sys
from json import load
from pathlib import Path

import requests

questions_path = sys.argv[1]

json_qs = Path(questions_path)
BASE_URL = "http://localhost:8000"
URL = f"{BASE_URL}/api/question"


def build_request_data(q: dict):
    print(f"BUILDING {q}")
    req_data = {
        "id": q["id"],
        "text": q["text_en"],
        "input_type": q["type"],
        "options": q.get("options"),
        "help_text": q.get("help_text"),
    }
    # i_type = None
    # match q["type"]:
    #     case "text":
    #         # class Text(BaseModel):
    #         #     i_type: Literal["text"]
    #         #     max_length: int | None = None
    #         req_data["type"] = "text"
    #     case "selection":
    #         # class Selection(BaseModel):
    #         #     i_type: Literal["selection"]
    #         #     options: list[str]
    #         opts = q["Options"]
    #         opts = opts.split(", ")
    #         i_type = {"i_type": "selection", "options": opts}
    #     case "multi-select" | "file upload" | "date-select":
    #         raise NotImplementedError(f"{q['Type']} not yet implemented!")
    #
    # {
    #   "id": "T1",
    #   "text": "Your name as shown on your professional profile (e.g. your university or research organisation profile",
    #   "required": "true",
    #   "input_type": {
    #     "i_type": "text"
    #   }
    # },
    # req_data["input_type"] = i_type
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
        print(f"SENDING {req_data}")
        res = requests.post(URL, json=req_data, timeout=5)
        if res.status_code != 200:
            if res.status_code == 422:
                print(f"[ERR]: {res.json()}")
                break
            if res.status_code == 500:
                print(f"[ERR]: {res.text}")
                break
            if res.status_code == 409:
                continue
            print(res.status_code)
            print(res.text)
