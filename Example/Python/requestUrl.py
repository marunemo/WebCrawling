# [ref] https://docs.python-requests.org/en/latest/

import requests

res = requests.get("https://www.google.co.kr", timeout=1)

print(res.status_code)
print(res.text)