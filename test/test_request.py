import requests as re

resp = re.post(
    url="http://0.0.0.0:80/chat",
    headers={
        "Authorization": "Bearer eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiaXNzIjoiQnV5bWVkLUFQIiwidG9rZW4iOiI1ZDJSVVhYUjNpcGRncHR3STFMTXExOVpacDJ3cGZSQmd4OUJjZU5MTXdsalFRQnQiLCJjbGllbnQiOiJxUkdlVzYyTW5GeldmVko5OXF6WWlydXdOdllldTU3cFhyeFFIMVZSZU0zWDFSclcifQo=",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
    },
    json=dict(
        question="có mấy loại voucher ở buymed?",
    ),
)
print(resp.text)
