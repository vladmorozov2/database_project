from sqlalchemy import create_engine,Column,Integer,Unicode,UnicodeText,String,ForeignKey,text
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("postgresql://postgres:1111@localhost/proj_db")
Session = sessionmaker(bind = engine)
Base = declarative_base()
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    decks = relationship('Deck', back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

    @classmethod
    def user_create(cls:object,name:str, email:str, password:str) -> object:
        user = cls(name = name,email = email,password = password)
        session.add(user)
        session.commit()
        return user
    
    @classmethod
    def user_get_by_id(cls,user_id):
        user =  session.query(cls).filter_by(id=user_id).first()
        return user
    
    @classmethod
    def user_update_name(cls,user_id, name) -> object:
        user = cls.user_get_by_id(user_id)
        user.name = name
        session.commit()
        return cls.user_get_by_id(user_id)
    
    @classmethod
    def user_change_password(cls,user_id, old_password, new_password) -> bool:
        user = session.query(cls).filter_by(id=user_id).first()
        if user == None or old_password != user.password:
            return False
        user.password = new_password
        session.commit()
        return True
    
    @classmethod
    def user_delete_by_id(cls,user_id:int) -> bool:
        
        user = session.query(cls).filter_by(id=user_id).first()
        if user ==None:
            return False
        session.delete(user)
        session.commit()
        return True
        
    
class Deck(Base):
    __tablename__ = 'decks'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(255))
    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship('User',back_populates='decks')
    cards = relationship('Card', back_populates='deck')
    
    def __repr__(self):
        return f"<Deck(id={self.id}, name='{self.name}', user_id={self.user_id})>"
    
    @classmethod
    def deck_create(cls,name, user_id) -> object: 
        deck_ = cls(name = name,user_id = user_id)
        session.add(deck_)
        session.commit()
        return deck_
    
    @classmethod
    def deck_get_by_id(cls,deck_id):
        deck =  session.query(cls).filter_by(id=deck_id).first()
        return deck
    
    @classmethod
    def deck_update(cls,deck_id, name) -> object:
        deck = cls.deck_get_by_id(deck_id)
        deck.name = name
        session.commit()
        return cls.deck_get_by_id(deck_id)
    
    @classmethod
    def deck_delete_by_id(cls,deck_id) -> bool:
        deck = cls.deck_get_by_id(deck_id)
        if deck == None:
            return False
        session.delete(deck)
        session.commit()
        return True
        
class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer,primary_key=True)
    word = Column(String)
    translation = Column(String)
    tip = Column(String)
    deck_id = Column(Integer, ForeignKey('decks.id'))  
    deck = relationship('Deck', back_populates='cards')
    
    
    def __repr__(self):
        return f"<Card(id={self.id}, user_id={self.user_id}, word='{self.word}', " \
               f"translation='{self.translation}', tip='{self.tip}')>"

    @classmethod
    def card_create(cls, word, translation, tip, deck_id=None):
        card = cls( word=word, translation=translation, tip=tip, deck_id=deck_id)
        session.add(card)
        session.commit()
        return card
    @classmethod
    def card_get_by_id(cls,card_id):
        card =  session.query(cls).filter_by(id=card_id).first()
        return card
    @classmethod
    def card_filter(cls, sub_word):
        query = session.query(cls).filter(
            text("word LIKE :sub_word OR translation LIKE :sub_word OR tip LIKE :sub_word")
        ).params(sub_word=f"%{sub_word}%")

        result = query.all()
        return tuple(result)
    @classmethod
    def card_update(cls,card_id, word=None, translation=None, tip=None):
        card_  = cls.card_get_by_id(card_id=card_id)
        if word != None:
            card_.word= word
        if translation != None:
            card_.translation = translation
        if tip != None:
            card_.tip = tip
        session.commit()
        return cls.card_get_by_id(card_id)
    @classmethod        
    def card_delete_by_id(cls,card_id) -> bool:
        card_ = cls.card_get_by_id(card_id)
        if card_ == None:
            return False
        session.delete(card_)
        session.commit()
        return True
    
        
        
        
Base.metadata.create_all(engine)
if __name__ == '__main__':
    
    pass

    

