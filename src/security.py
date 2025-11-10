from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
