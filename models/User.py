from models.Base import db
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String, Float, update, Integer, Text, select, delete, asc
from datetime import datetime,timezone
from hashlib import md5
import enum
from app_class.user_class import UserData
from flask_login import UserMixin, login_user


class UserRole(enum.Enum):
    USER = 'user'
    ADMIN = 'admin'

class UserStatus(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'





class User(db.Model,UserMixin):
    __tablename__='users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False,unique=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[UserRole] = mapped_column(String(20), nullable=False, default='user')
    status: Mapped[UserStatus] = mapped_column(String(20), nullable=False, default='active')
    has_edit_access: Mapped[UserStatus] = mapped_column(String(20), nullable=True, default='no')
    is_author: Mapped[UserStatus] = mapped_column(String(10), nullable=True, default='no')
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc),
                                                 onupdate=datetime.now(timezone.utc))

    # foreign key
    posts_added= relationship('BlogPost', back_populates='added_by', lazy=True,
                         foreign_keys='BlogPost.added_by_id')
    posts_updated= relationship('BlogPost', back_populates='updated_by', lazy=True,
                         foreign_keys='BlogPost.updated_by_id')
    comments = relationship('Comment', back_populates='comment_by', lazy=True,
                            cascade='all, delete-orphan')

    def avatar(self, size=80):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=wavatar&s={size}'

    def is_admin(self):
        """Check if THIS user is admin"""
        current_role = db.session.execute(
            select(User.role).where(User.id == self.id)
        ).scalar()
        return current_role == 'admin'

    def edit_access(self):
        """Check if THIS user is admin"""
        edit_access = db.session.execute(
            select(User.has_edit_access).where(User.id == self.id)
        ).scalar()
        return edit_access == 'yes'

    def check_is_author(self):
        """Check if THIS user is admin"""
        is_author = db.session.execute(
            select(User.is_author).where(User.id == self.id)
        ).scalar()
        return is_author == 'yes'

    @classmethod
    def addUser(cls,form_obj:UserData):
        new_user=cls(
            name=form_obj.name,
            email=form_obj.email,
            password=form_obj.password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

    @classmethod
    def getByParam(cls,**kwargs):
        return cls.query.filter_by(**kwargs).first()