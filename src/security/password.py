import os
from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=int(os.getenv("ARGON2_TIME", 3)),
    memory_cost=int(os.getenv("ARGON2_MEMORY", 65536)),
    parallelism=int(os.getenv("ARGON2_PARALLELISM", 1)),
    hash_len=int(os.getenv("ARGON2_HASH_LEN", 32)),
)

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(stored_hash: str, password: str) -> bool:
    return ph.verify(stored_hash, password)
