from sqlalchemy.orm import Session


from transitions.extensions import GraphMachine as Machine

from . import models, schemas

# TODO: Mixin model (Status Class)
states=['solid', 'liquid', 'gas', 'plasma']

# And some transitions between states. We're lazy, so we'll leave out
# the inverse phase transitions (freezing, condensation, etc.).
transitions = [
    { 'trigger': 'melt', 'source': 'solid', 'dest': 'liquid' },
    { 'trigger': 'evaporate', 'source': 'liquid', 'dest': 'gas' },
    { 'trigger': 'sublimate', 'source': 'solid', 'dest': 'gas' },
    { 'trigger': 'ionize', 'source': 'gas', 'dest': 'plasma' },
    { 'trigger': 'proscia', 'source': 'solid', 'dest': 'plasma' },
    { 'trigger': 'deproscia', 'source': 'plasma', 'dest': 'solid' }
]


def get_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    # machine = Machine(model=db_user, states=states, initial=db_user.state, transitions=transitions)

    return db_user




def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(models.User.email == email).first()




def get_users(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.User).offset(skip).limit(limit).all()



def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, user_state=user.user_state)
    print(dir(db_user))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_items(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Item).offset(skip).limit(limit).all()



def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
