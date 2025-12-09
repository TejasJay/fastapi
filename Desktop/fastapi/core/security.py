from passlib.context import CryptContext

# Initialize CryptContext with bcrypt scheme
# Use lazy initialization to avoid errors during import
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except Exception:
    # Fallback if bcrypt initialization fails
    # This should not happen if bcrypt is properly installed
    raise ImportError("bcrypt is required. Install it with: pip install bcrypt")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)