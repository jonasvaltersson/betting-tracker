from sqlalchemy import (
    Column, Integer, BigInteger, String, Date
)

from app.db import Base, Session


class Bet(Base):
    __tablename__ = 'bet'

    id = Column(Integer, primary_key=True)
    user_id = Column(String())
    amount = Column(Integer())
    exponent = Column(Integer())
    currency = Column(String())
    category = Column(String())
    status = Column(String())
    result = Column(String())

    @classmethod
    def create(cls, user_id, body):
        body.update({'user_id': user_id})
        bet = Bet(**body)
        bet.save()
        return bet

    @classmethod
    def get(cls, user_id, bet_id):
        query = Session.query(cls)
        query = query.filter(
            Bet.user_id == user_id,
            Bet.id == bet_id
        )
        return query.one()

    @classmethod
    def update(cls, **kwargs):
        user_id = kwargs.get('user_id')
        bet_id = kwargs.get('id')
        updated_bet = kwargs.get('data')

        bet = cls.get(user_id, bet_id)
        bet_dict = bet.to_dict()
        
        for key, value in updated_bet.items():
            bet_dict[key] = value
        return bet_dict