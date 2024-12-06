from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from . import database, models, auth
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "YOUR_SECRET_KEY"  # Change it to os.getenv('SECRET_KEY')
ALGORITHM = "HS256"

#
# Token Life Span
ACCESS_TOKEN_EXPIRE_MINUTES = 30    # In minutes
# Change it to what's suitable for the usecase
#

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db() -> Session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


class JWTAuthManager:
    def __init__(self, secret_key: str, algorithm: str, token_expiry_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiry_minutes = token_expiry_minutes

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def _decode_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    def get_current_user(self, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> models.User:
        token_data = self._decode_access_token(token)
        username: str = token_data.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = db.query(models.User).filter(models.User.username == username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user


auth_manager = JWTAuthManager(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)
