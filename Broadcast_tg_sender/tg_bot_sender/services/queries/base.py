from uuid import UUID, uuid4


class BaseService:
    @staticmethod
    def generate_id() -> UUID:
        return uuid4()