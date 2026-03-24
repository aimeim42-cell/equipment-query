import urllib.request
import json

data = json.dumps({
    "description": "工单数据备份",
    "public": False,
    "files": {
        "workorders.json": {"content": '{"workorders":[],"updateTime":"2026-03-23"}'}
    }
}).encode("utf-8")

req = urllib.request.Request(
    "https://api.github.com/gists",
    data=data,
    method="POST",
    headers={
        "Authorization": "token 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",
        "Content-Type": "application/json"
    }
)

try:
    r = urllib.request.urlopen(req)
    result = json.loads(r.read().decode())
    print("SUCCESS!")
    print("Gist ID:", result["id"])
    print("URL:", result["html_url"])
except Exception as e:
    print("Error:", e)
    if hasattr(e, "read"):
        print(e.read().decode())
