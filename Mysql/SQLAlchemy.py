import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, validates
from sqlalchemy.pool import QueuePool
from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.event import listens_for
from sqlalchemy import Column, Integer, String, Index

engine = create_engine(
    'mysql://root:xxxx@127.0.0.1/test?charset=utf8mb4',
    convert_unicode=True,
    echo=False,
    poolclass=QueuePool,
    pool_size=200,
    pool_recycle=100,
    max_identifier_length=128
)
session = scoped_session(sessionmaker(bind=engine))
class_registry = {}
Base = declarative_base(class_registry=class_registry)


class BaseModel(AbstractConcreteBase, Base):
    id = Column(Integer, primary_key=True)


class User(BaseModel):
    __tablename__ = 'user'

    name = Column(String(20), name='name')
    ix_name = Index('ix_name', name)

    @hybrid_property
    def fullname(self):
        return f'User:{self.name}'

    @validates('name')
    def validate_name(self, _, user):
        assert isinstance(user, str)
        return user


if __name__ == '__main__':
    print(sqlalchemy.__version__)

    Base.metadata.create_all(engine)
    _user = User(name='严梓桓')
    session.add(_user)
    print(session.new)
    session.commit()
    print(session.dirty)

    _user1 = session.query(User).filter_by(name='严梓桓').first()
    print(_user1.id, ':', _user1.name, ':', _user1.fullname)

    _user1.name = '张三'
    flag_modified(_user1, 'name')
    print(session.dirty)
    session.commit()
    print(session.dirty)
