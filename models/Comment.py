from models.Base import db
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Integer, Text, select, delete, asc, ForeignKey, desc
from datetime import datetime,timezone
from app_class.comment_class import CommentData





# CONFIGURE TABLE
class Comment(db.Model):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc),
                                                 onupdate=datetime.now(timezone.utc))


    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    comment_by = relationship('User', back_populates='comments')


    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    post = relationship('BlogPost', back_populates='comments')

    @classmethod
    def addComment(cls, form_obj: CommentData):
        new_comment = cls(
            text=form_obj.text,
            post_id=form_obj.post_id,
            user_id=form_obj.user_id
        )
        db.session.add(new_comment)
        db.session.commit()


    @classmethod
    def getAllComment(cls,post_id):
        query=select(cls).where(cls.post_id==post_id).order_by(desc(cls.id))
        comments=db.session.execute(query).scalars()
        return comments.all()
