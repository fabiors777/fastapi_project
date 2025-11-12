from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os


load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")


bcrypt_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
oayth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")
