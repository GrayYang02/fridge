import jwt

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwODIyMTI0LCJpYXQiOjE3NDA4MjE4MjQsImp0aSI6ImJiYjM2NDhmNDZlMDRhZDliOGNiMTkzZTA0ZDE2NDgyIiwidXNlcl9pZCI6Mn0.Zlb0W4lqfQGeYOVbFkl6INxEsvAm8XUEkYGca9tQ0NA"

try:
    decoded = jwt.decode(token, options={"verify_signature": False})  # No secret key needed
    print(decoded)
except jwt.ExpiredSignatureError:
    print("Token expired!")
except jwt.DecodeError:
    print("Invalid token format!")
