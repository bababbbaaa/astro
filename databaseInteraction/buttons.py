from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
from posixpath import abspath
from os.path import join

LINK ='sqlite:///' + abspath(join('..', 'horoscope.db'))

engine = create_engine(LINK)
Session = sessionmaker(engine)()

Base = declarative_base()

class Button(Base):
    """
    
    Модель данных о кнопке в посте

    ID : int
    PostID - пост, в которой находится кнопка
    Source - надпись, указанная в кнопке
    Url - ссылка, указанная в кнопке

    """

    __tablename__ = 'Buttons'
    
    ID = Column(Integer, nullable=False, unique=True, primary_key=True)
    PostID = Column(String, nullable=False)
    Source = Column(String,nullable=False)
    Url = Column(String, nullable=False)

def drop_table():
    Button.__table__.drop(engine)

def add_button(
    _session : Session,
    post_id : int,
    source : str,
    url : str
) -> Button:

    markup = Button(
        PostID = post_id,
        Source = source,
        Url = url
    )

    _session.add(markup)
    _session.commit()

    return markup

def get_buttons(
    _session,
    post_id,
    *args,
    **kwargs
) -> list:
    
    buttons = select(Button).where(Button.PostID == post_id)

    return list(_session.scalars(buttons))

def _get_button(id):
    return select(Button).where(Button.ID == id)

def get_button(_session, id) -> Button:
    return _session.execute(_get_button(id)).scalar()

def update_button(
    _session : Session,
    id,
    post_id = None,
    source : str = None,
    url : str = None
) -> Button:

    button = get_button(_session, id)

    if post_id is not None:
        setattr(button, "PostID", post_id)

    if source is not None:
        setattr(button, "Source", source)

    if url is not None:
        setattr(button, "Url", url)

    _session.commit()

    return button

def delete_button(_session, button : Button) -> None:
    _session.delete(button)
    _session.commit()

Base.metadata.create_all(engine)
