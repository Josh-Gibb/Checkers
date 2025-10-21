from db import Database

db = Database()

class User_manager:
    # Validates user credentials to create user
    def create_user(self, username, password, confirm_password) -> tuple[bool, str]:
        if db.get_user(username) is not None:
            return False, "Username already exists"
        if len(username) < 3:
            return False, "Username too short"
        if len(password) < 6:
            return False, "Password too short"
        if password != confirm_password:
            return False, "Passwords do not match"
        db.create_user(username, password)
        return True, "Successfully created new user"

    # Validates user credentials to login
    def verify_login(selfs, username, password) -> tuple[bool, str]:
        if db.get_user(username) is None:
            return False, "Incorrect credentials"
        if db.correct_password(username, password):
            return False, "Incorrect credentials"
        return True, "Successfully logged in"
