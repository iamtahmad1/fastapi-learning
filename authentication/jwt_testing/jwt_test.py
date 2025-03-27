#import jwt
import datetime
import jwt
import time

SECRET_KEY="TESTSECRET"

payload={
    "user_id": 123,
    "role": "admin",
    "iat": datetime.datetime.utcnow(),
    "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=20)

}


token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print("Generated JWT TOKEN:", token)

#time.sleep(30)
try:
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    print("Decoded Payload:", decoded_payload)
except jwt.ExpiredSignatureError:
    print("Token has expired!")
except jwt.InvalidTokenError:
    print("Invalid Token!")
