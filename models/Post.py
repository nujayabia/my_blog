import enum

from models.Base import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, update, Integer, Text, select, delete, asc, ForeignKey
from datetime import datetime,timezone
from app_class.post_class import PostData

class BlogStatus(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'




# CONFIGURE TABLE
class BlogPost(db.Model):
    __tablename__='posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=True)
    status: Mapped[BlogStatus] = mapped_column(String(20), nullable=True, default='active')
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc),
                                                 onupdate=datetime.now(timezone.utc))

    #foreign keys
    added_by_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    added_by = relationship('User', foreign_keys=[added_by_id], back_populates='posts_added')

    updated_by_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    updated_by = relationship('User', foreign_keys=[updated_by_id], back_populates='posts_updated')

    comments = relationship('Comment', back_populates='post', lazy=True,
                            cascade='all, delete-orphan')






    @classmethod
    def getAll(cls):
        query=select(cls).order_by(asc(cls.title))
        posts=db.session.scalars(query)
        return posts.all()

    @classmethod
    def getQuery(cls):
        return db.session.query(cls).order_by(cls.date.desc())

    @classmethod
    def get_query_by_user(cls, user_id):
        """Returns a query object filtered by user, can be chained with .paginate()"""
        return db.session.query(cls).where(cls.added_by_id == user_id).order_by(cls.date.desc())

    @classmethod
    def getAllPostUser(cls, user_id):
        """Returns all posts by a specific user as a list"""
        return cls.get_query_by_user(user_id).all()

    @classmethod
    def addPost(cls,form_obj:PostData):
        new_post=cls(
            title=form_obj.title,
            subtitle=form_obj.subtitle,
            date=form_obj.date,
            body=form_obj.body,
            author=form_obj.author,
            img_url=form_obj.img_url,
            added_by_id=form_obj.added_by_id
        )
        db.session.add(new_post)
        db.session.commit()


    @classmethod
    def editPost(cls,form_obj:PostData,post_id):
        post=cls.getPost(post_id)
        if post:
            post.title=form_obj.title
            post.subtitle = form_obj.subtitle
            post.body = form_obj.body
            post.author = form_obj.author
            post.img_url = form_obj.img_url
            post.updated_by_id = form_obj.updated_by_id
        db.session.commit()


    @classmethod
    def deletePost(cls,post_id):
        query=delete(cls).where(cls.id==post_id)
        db.session.execute(query)
        db.session.commit()


    @classmethod
    def getPost(cls,post_id):
        query=select(cls).where(cls.id==post_id)
        post_data=db.session.scalar(query)
        print(post_data)
        return post_data

