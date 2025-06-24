from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
hashed_password = bcrypt.generate_password_hash("").decode('utf-8')
print("Hashed Password:", hashed_password)
