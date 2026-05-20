from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text

class Base(DeclarativeBase):
    pass

#creates database
db = SQLAlchemy(model_class=Base)

