from sqlalchemy.orm import Session

from src.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self):
        return self.db.query(User).all()
    
    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_id(self, id: int):
        return self.db.query(User).filter(User.id == id).first()

    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
