import pytest

from app.persistence.bet import Bet


@pytest.fixture
def bet_dict():
    return dict(
        user_id='00000000-0000-0000-0000-000000000001',
        id=1,
        amount=1000,
        exponent=2,
        currency='SEK',
        category='football',
        status='pending',
        result='loss'
    )   

@pytest.fixture
def bet(user_id, bet_dict):
    bet = Bet(**bet_dict)
    bet.save()

@pytest.fixture
def user_id():
    return '00000000-0000-0000-0000-000000000001'