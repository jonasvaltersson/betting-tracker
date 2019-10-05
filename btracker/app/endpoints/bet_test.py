import pytest


def test_create_bet(test_client, bet_dict, user_id):
    response = test_client.post(f'v1/{user_id}/bet', json=bet_dict).json
    assert response['user_id'] == '00000000-0000-0000-0000-000000000001'
    assert response['id'] == 1

def test_update_pending_bet_to_finished_bet(test_client, bet, bet_dict, user_id):
    # GIVEN a updated bet
    bet_dict['amount'] = 250
    bet_dict['currency'] = 'NOK'
    bet_dict['status'] = 'done'

    # WHEN I attempt to update fields on the bet
    response = test_client.put(f'v1/{user_id}/bet/1', json=bet_dict).json
    
    # THEN the bet should be updated with the correct fields
    assert response['amount'] == 250
    assert response['currency'] == 'NOK'
    assert response['category'] == 'football'
    assert response['status'] == 'done'
    assert response['user_id'] == '00000000-0000-0000-0000-000000000001'
    assert response['id'] == 1

def test_get_bet(test_client, bet, user_id):
    response = test_client.get(f'v1/{user_id}/bet/1').json
    assert response['id'] == 1

def test_get_bets(test_client, bet, user_id):
    pass
    
def test_get_bet(test_client):
    pass

def test_filter_bets_by_category(test_client):
    pass

def test_filter_bets_by_result(test_client):
    pass

def test_filter_bets_by_status(test_client):
    pass

