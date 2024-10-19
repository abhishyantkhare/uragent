from sqlalchemy.orm import Session, sessionmaker


class BaseStore:

    def __init__(self, session_maker: sessionmaker[Session]):
        self._session_maker = session_maker

    def session(self):
        return self._session_maker.begin()
