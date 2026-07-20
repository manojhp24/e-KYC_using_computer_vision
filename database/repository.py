import numpy as np
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import User


class UserRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def _embedding_to_bytes(self, embedding: np.ndarray) -> bytes:

        return embedding.astype(np.float64).tobytes()

    def _bytes_to_embedding(self, embedding_bytes: bytes) -> np.ndarray:

        return np.frombuffer(embedding_bytes, dtype=np.float64)

    def get_user_by_id_number(self, id_number: str) -> User | None:

        logger.info(f"Searching user ID:{id_number}")

        user = self.db.query(User).filter(User.id_number == id_number).first()

        if user:
            logger.success("User found")
        else:
            logger.warning("User not found")

        return user

    def user_exists(self, id_number: str) -> bool:

        exists = self.get_user_by_id_number(id_number) is not None

        logger.info(f"User exists for ID '{id_number}': {exists}")

        return exists

    def create_user(
        self,
        name: str,
        id_number: str,
        id_type: str,
        date_of_birth: str,
        gender: str,
        address: str | None,
        face_embedding: np.ndarray,
    ) -> User:

        embedding_bytes = self._embedding_to_bytes(face_embedding)

        user = User(
            name=name,
            id_number=id_number,
            id_type=id_type,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            face_embedding=embedding_bytes,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_all_face_embeddings(self) -> list[tuple[User, np.ndarray]]:

        users = self.db.scalars(select(User)).all()

        embeddings = [
            (user, self._bytes_to_embedding(user.face_embedding)) for user in users
        ]

        logger.info(f"Loaded {len(embeddings)} face embeddings.")

        return embeddings
