import bcrypt

class Hash:
    @staticmethod
    def bcrypt(password: str) -> str:
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pwd_bytes, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        try:
            pwd_bytes = plain_password.encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(pwd_bytes, hashed_bytes)
        except ValueError as e:
            print(f"DEBUG: Password verification error (Invalid Salt): {str(e)}")
            return False
        except Exception as e:
            print(f"DEBUG: Unexpected error in password verification: {str(e)}")
            return False
