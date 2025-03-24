from sqlalchemy.orm import Session
from faker import Faker
from database import SessionLocal
from database import Users

# Initialize Faker to generate random user data
fake = Faker()

# Get a new database session
db: Session = SessionLocal()

# Insert 10 fake users
users = []
for user in range(20, 10000):
    user = Users(id=user,name=fake.name(), email=fake.email())
    users.append(user)

# Add users to the database
db.add_all(users)
db.commit()

# Print confirmation
print("✅ 10 users inserted successfully!")

# Close the session
db.close()
