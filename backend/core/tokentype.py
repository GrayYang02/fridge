import jwt
import time
from datetime import datetime
from django.conf import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django
django.setup()
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQzMTU5OTM0LCJpYXQiOjE3NDMxNTYzOTQsImp0aSI6IjEwODU3YzVkNmJmMzRmYzA5YzBiZGZlMDBhNDE0MGQyIiwidXNlcl9pZCI6Mn0.gaNLi0mJTPZottnsEmKCbwM7hLo4pBQSvZNThnBbb4o"

try:
    print(settings.SIMPLE_JWT)
    decoded = jwt.decode(token, options={"verify_signature": False})  # No secret key needed
    print(decoded)
    iat = decoded.get("iat")
    exp = decoded.get("exp")

    now = int(time.time())
    remaining = exp - now
    remaining_seconds = exp - now
    remaining_minutes = round(remaining_seconds / 60, 2)

    print("issued (iat):", datetime.fromtimestamp(iat))
    print("expired (exp):", datetime.fromtimestamp(exp))
    print("current:", datetime.fromtimestamp(now))
    print("remaining seconds:", remaining_seconds)
    print("remaining minutes:", remaining_minutes)
except jwt.ExpiredSignatureError:
    print("Token expired!")
except jwt.DecodeError:
    print("Invalid token format!")
