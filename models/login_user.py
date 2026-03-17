import hashlib

class LoginUser:

    def __init__(self, email, password, role):
        self.email = email
        self.password = self.encrypt_password(password)
        self.role = role

    def encrypt_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password == hashlib.sha256(password.encode()).hexdigest()

    def login(self):
        print("User logged in:", self.email)

    def logout(self):
        print("User logged out")