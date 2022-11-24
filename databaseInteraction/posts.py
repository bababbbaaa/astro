from datetime import datetime
from sqlalchemy import *

from sqlalchemy.orm import sessionmaker
from controller import Base, engine

Session = sessionmaker(engine)()

DATE_FORMAT = '%d.%m.%Y'
TIME_FORMAT = '%H:%M'


class Post(Base):
    """

    Модель запланированный пост в базе данных
    ID : int
    category : str
    date : str
    time : str
    managerID : int
    postID : int


    """

    __tablename__ = 'Posts'

    ID = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    Category = Column(String, nullable=False)
    Time = Column(String, nullable=False)
    Date = Column(Integer, nullable=False)
    ManagerID = Column(String, nullable=False)
    PostID = Column(String, nullable=False)
    FirstRow = Column(String, nullable=False)
    FilePath = Column(String,)


def drop_table():
    Post.__table__.drop(engine)


def add_post(
        _session,
        category: str,
        managerId: int,
        postId: int,
        date: str,
        first_row: str,
        path: str,
        time: str = None) -> Post:
    """ Создание нового поста """

    date = datetime.strptime(date, DATE_FORMAT)
    date = datetime.strftime(date, DATE_FORMAT)

    time = datetime.strptime(time, TIME_FORMAT)
    time = datetime.strftime(time, TIME_FORMAT)

    post = Post(
        Category=category,
        Time=time,
        ManagerID=managerId,
        PostID=postId,
        Date=date,
        FirstRow=first_row, FilePath=path)

    _session.add(post)
    _session.commit()

    return post


def get_posts(_session, date: str = None, category: str = None, time: str = None, *args, **kwargs) -> list:
    """ 

    Получение постов по определенным критериям 

    :return: list[Post]
    """

    posts = _get_posts(date, category, time)
    return list(_session.scalars(posts))


def _get_posts(
        date: str = None,
        category: str = None,
        time: str = None,
        *args,
        **kwargs) -> list:

    posts = select(Post)

    if date:
        date = datetime.strptime(date, DATE_FORMAT)
        date = datetime.strftime(date, DATE_FORMAT)
        posts = posts.where(Post.Date == date)

    if category:
        posts = posts.where(Post.Category == category)

    if time:
        time = datetime.strptime(time, TIME_FORMAT)
        time = datetime.strftime(time, TIME_FORMAT)

        posts = posts.where(Post.Time == time)

    return posts


def _get_post(id):

    return select(Post).where(Post.PostID == id)


def get_post(_session, id) -> Post:
    """" 

    Получение поста по определенным критериям

    :return: Post
    """

    return _session.execute(_get_post(id)).scalar()


def update_post(
    _session,
    id,
    new_id: int = None,
    category: str = None,
    time: str = None,
    date: str = None,
    first_row: str = None
) -> None:

    post = get_post(_session, id)

    if new_id is not None:
        setattr(post, "PostID", new_id)

    if category is not None:
        setattr(post, "Category", category)

    if time is not None:
        time = datetime.strptime(time, TIME_FORMAT)
        time = datetime.strftime(time, TIME_FORMAT)

        setattr(post, "Time", time)

    if date is not None:
        date = datetime.strptime(date, DATE_FORMAT)
        date = datetime.strftime(date, DATE_FORMAT)

        setattr(post, "Date", date)

    if first_row is not None:
        setattr(post, "FirstRow", first_row)

    _session.commit()

    return


def delete_post(_session, post) -> None:
    _session.delete(post)
    _session.commit()


Base.metadata.create_all(engine)
