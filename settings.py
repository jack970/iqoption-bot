import os
SECRET_KEY = os.getenv("USER")
DATABASE_PASSWORD = os.getenv("PASS")

print(SECRET_KEY)