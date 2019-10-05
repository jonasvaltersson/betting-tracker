from app.persistence.bet import Bet 


def create(**kwargs):
    user_id = kwargs.get('user_id')
    body = kwargs.get('data')

    bet = Bet.create(user_id, body)
    return bet.to_dict()


def update(**kwargs):
    bet = Bet.update(**kwargs)
    return bet


def get(**kwargs):
    user_id = kwargs.get('user_id')
    bet_id = kwargs.get('bet_id')

    bet = Bet.get(user_id, bet_id)
    return bet.to_dict()
