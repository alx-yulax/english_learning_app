from sqlalchemy import select

from app.database.models import User
from app.database.session import get_session


class UsersService:
    @staticmethod
    def get_or_create_user(
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
    ) -> User:
        if not isinstance(telegram_id, int):
            raise ValueError("telegram_id must be int")

        with get_session() as session:
            stmt = select(User).where(User.telegram_id == telegram_id)
            user = session.scalar(stmt)

            if user:
                return user

            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
            )
            session.add(user)
            session.flush()  # получаем user.id

            return user
