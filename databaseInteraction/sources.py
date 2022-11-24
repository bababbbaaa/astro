from sqlalchemy import *
from controller import engine, Base, Session
from utils import *


class Source(Base):
    """

    Модель источника прихода пользователя в бд

    ID : int
    title : str
    code : string
    price : int

    """

    __tablename__ = "Sources"

    ID = Column(Integer, nullable=False, unique=True, primary_key=True)
    title = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    date = Column(Text, nullable=False)
    type = Column(Text, nullable=False)


def drop_table():
    Source.__table__.drop(engine)


def add_source(
        title: str,
        code: str,
        price: int,
        date : str,
        type : str) -> Source:

    if not basic_check_date(date):
        raise Exception("Invalid date")

    source = Source(
        title=title,
        code=code,
        price=price,
        date=date,
        type=type
    )

    Session.add(source)
    Session.commit()

    return source


def update_source(code, new_title: str) -> None:
    """

    Меняет название источника

    """
    source = get_source(code)

    setattr(source, "title", new_title)
    Session.commit()

    return


def delete_source(code: str = None, title: str = None) -> None:
    source = get_source(code, title)

    if source is not None:
        Session.delete(source)
        Session.commit()
        return

def get_sources(title: str = None) -> list:
    sources = _get_sources(title)
    return list(Session.scalars(sources))


def get_source(code: str = None, title: str = None) -> Source:
    """

    Получение объекта источника по его уникальному коду

    """

    source = _get_source(code, title)
    if source is not None:
        return Session.execute(source).scalar()


def _get_source(code: str, title: str):
    if code is not None:
        print(code)
        return select(Source).where(Source.code == code)

    return select(Source).where(Source.title == title)


def _get_sources(title) -> list:
    sources = select(Source)

    if title is not None:
        sources = sources.where(Source.title == title)

    return sources

Base.metadata.create_all(engine)
