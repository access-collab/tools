from json import load
from pathlib import Path
import requests

vlopse = "tiktok"
json_qs = Path(f"tests/resources/{vlopse}_questions.json")
BASE_URL = "http://localhost:8000"
URL = f"{BASE_URL}/api/vlopse/{vlopse}/question"
with open(json_qs) as f:
    qs = load(f)
    print(f"Found {len(qs)} questions, adding them..")
    for i, q in enumerate(qs):
        res = requests.post(URL, json=q, timeout=5)
        print(res.status_code)
