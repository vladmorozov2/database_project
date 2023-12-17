from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import Session, sessionmaker, relationship
from main import User, Deck, Card

# Create an SQLite in-memory database for testing
engine = create_engine("postgresql://postgres:1111@localhost/proj_db")

# Bind the engine to the session
Session = sessionmaker(bind=engine)
session = Session()

# Update your existing code to use the in-memory database
User.metadata.create_all(engine)
Deck.metadata.create_all(engine)
Card.metadata.create_all(engine)

def test_user_crud():
    # Test user creation
    user = User.user_create(name="John Doe", email="john@example.com", password="password123")
    assert user.id is not None

    # Test user retrieval
    retrieved_user = User.user_get_by_id(user.id)
    assert retrieved_user == user

    # Test user update
    updated_user = User.user_update_name(user.id, "John Updated")
    assert updated_user.name == "John Updated"

    # Test user change password
    assert User.user_change_password(user.id, "password123", "newpassword")
    assert not User.user_change_password(user.id, "wrongpassword", "newpassword")

    # Test user deletion
    # assert User.user_delete_by_id(user.id)
    # assert not User.user_delete_by_id(user.id)

def test_deck_crud():
    # Create a user for testing
    user = User.user_create(name="Test User", email="test@example.com", password="testpassword")

    # Test deck creation
    deck = Deck.deck_create(name="Test Deck", user_id=user.id)
    assert deck.id is not None

    # Test deck retrieval
    retrieved_deck = Deck.deck_get_by_id(deck.id)
    assert retrieved_deck == deck

    # Test deck update
    updated_deck = Deck.deck_update(deck.id, "Updated Deck")
    assert updated_deck.name == "Updated Deck"

    # Test deck deletion
    assert Deck.deck_delete_by_id(deck.id)
    assert not Deck.deck_delete_by_id(deck.id)

def test_card_crud():
    # Create a user and a deck for testing
    user = User.user_create(name="Test User", email="test@example.com", password="testpassword")
    deck = Deck.deck_create(name="Test Deck", user_id=user.id)

    # Test card creation
    card = Card.card_create(word="Test Word", translation="Test Translation", tip="Test Tip", deck_id=deck.id)
    assert card.id is not None

    # Test card retrieval
    retrieved_card = Card.card_get_by_id(card.id)
    assert retrieved_card == card

    # Test card update
    updated_card = Card.card_update(card.id, word="Updated Word", translation="Updated Translation", tip="Updated Tip")
    assert updated_card.word == "Updated Word"
    assert updated_card.translation == "Updated Translation"
    assert updated_card.tip == "Updated Tip"

    # Test card deletion
    assert Card.card_delete_by_id(card.id)
    assert not Card.card_delete_by_id(card.id)
def test_card_filter():
    # Create a user and a deck for testing
    user = User.user_create(name="Test User", email="test@example.com", password="testpassword")
    deck = Deck.deck_create(name="Test Deck", user_id=user.id)

    # Create some sample cards
    card1 = Card.card_create(word="Apple", translation="Pomme", tip="Fruit", deck_id=deck.id)
    card2 = Card.card_create(word="Banana", translation="Banane", tip="Fruit", deck_id=deck.id)
    card3 = Card.card_create(word="Carrot", translation="Carotte", tip="Vegetable", deck_id=deck.id)

    # Test card filtering with a search term
    result = Card.card_filter("Ban")
    assert card2 in result
    assert card1 not in result
    assert card3 not in result

    # Test card filtering with a different search term
    result = Card.card_filter("Vegetable")
    assert card3 in result
    assert card1 not in result
    assert card2 not in result

if __name__ == '__main__':
    test_user_crud()
    test_deck_crud()
    test_card_crud()
    test_card_filter()

    print("All tests passed!")
