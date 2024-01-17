from sqlalchemy import Table, Boolean, Column, Integer, String
from database import Base


class Todo(Base):
    __tablename__ = "todo"
    todo_id = Column(Integer, primary_key=True)
    todo_title = Column(String(50))
    todo_description = Column(String(50))
    completed = Column(Boolean, default=False)
