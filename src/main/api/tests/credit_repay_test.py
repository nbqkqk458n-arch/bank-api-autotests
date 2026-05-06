import pytest
import requests
@pytest.mark.api
class TestRepayCredit:
    def test_repay_credit_valid(self):
        login_admin_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                'accept': 'application / json',
                'Content-Type': 'application/json'
            }
        )
        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get('token')

        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json={
                "username": "Max520",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'

            }
        )
        assert create_user_response.status_code == 200
        assert create_user_response.json().get('role') == 'ROLE_CREDIT_SECRET'

        login_user_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json={
                "username": "Max520",
                "password": "Pas!sw0rd"
            },
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )
        assert login_user_response.status_code == 200
        token = login_user_response.json().get('token')

        create_account_response = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application / json',
                'Authorization': f'Bearer {token}'
            }
        )
        assert create_account_response.status_code == 201
        assert create_account_response.json().get('balance') == 0

        account_id = create_account_response.json().get('id')

        credit_request_response = requests.post(
            url='http://localhost:4111/api/credit/request',
            json={
                "accountId": account_id,
                "amount": 5000,
                "termMonths": 12
            },
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )
        assert credit_request_response.status_code == 201
        assert credit_request_response.json().get('balance') == 5000
        credit_id = credit_request_response.json().get('creditId')

        credit_repay_request = requests.post(
            url='http://localhost:4111/api/credit/repay',
            json={
                "creditId": credit_id,
                "accountId": account_id,
                "amount": 5000
            },
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }

        )
        assert credit_repay_request.status_code == 200
        assert credit_repay_request.json().get('amountDeposited') == 5000
    def test_repay_credit_invalid(self):
        login_admin_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                'accept': 'application / json',
                'Content-Type': 'application/json'
            }
        )
        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get('token')

        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json={
                "username": "Max530",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'

            }
        )
        assert create_user_response.status_code == 200
        assert create_user_response.json().get('role') == 'ROLE_CREDIT_SECRET'

        login_user_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json={
                "username": "Max530",
                "password": "Pas!sw0rd"
            },
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )
        assert login_user_response.status_code == 200
        token = login_user_response.json().get('token')

        create_account_response = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application / json',
                'Authorization': f'Bearer {token}'
            }
        )
        assert create_account_response.status_code == 201
        assert create_account_response.json().get('balance') == 0

        account_id = create_account_response.json().get('id')

        credit_request_response = requests.post(
            url='http://localhost:4111/api/credit/request',
            json={
                "accountId": account_id,
                "amount": 5000,
                "termMonths": 12
            },
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )
        assert credit_request_response.status_code == 201
        assert credit_request_response.json().get('balance') == 5000
        credit_id = credit_request_response.json().get('creditId')

        credit_repay_request = requests.post(
            url='http://localhost:4111/api/credit/repay',
            json={
                "creditId": credit_id,
                "accountId": account_id,
                "amount": 6000
            },
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }

        )
        assert credit_repay_request.status_code == 422
