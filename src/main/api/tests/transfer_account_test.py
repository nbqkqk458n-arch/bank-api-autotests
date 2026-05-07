from src.main.api.models.deposit_account_request import DepositAccountRequest
import pytest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.deposit_account_requester import DepositAccountRequester
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.requests.transfer_account_requester import TransferAccountRequester
@pytest.mark.api
class TestTransferAccount:
    def test_transfer_account_valid(self):
        create_user_request = CreateUserRequest(username='Max909', password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        login_user_request = LoginUserRequest(username='Max909', password='Pas!sw0rd')

        LoginUserRequester(
            request_spec=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()

        ).post(login_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Max909', password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()


        response2 = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Max909', password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        deposit_account_request = DepositAccountRequest(accountId=response.id, amount=1000)

        response = DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Max909', password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()

        ).post(deposit_account_request)


        transfer_account_request = TransferAccountRequest(fromAccountId=response.id,toAccountId=response2.id, amount= 500)

        response = TransferAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Max909',password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_account_request)

        assert response.fromAccountIdBalance == 500


    def test_transfer_account_invalid(self):
        create_user_request = CreateUserRequest(username='Max910', password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        login_user_request = LoginUserRequest(username='Max910', password='Pas!sw0rd')

        LoginUserRequester(
            request_spec=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()

        ).post(login_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Max910', password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        response2 = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Max910', password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        deposit_account_request = DepositAccountRequest(accountId=response.id, amount=1000)

        response = DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Max910', password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()

        ).post(deposit_account_request)

        transfer_account_request = TransferAccountRequest(fromAccountId=response.id, toAccountId=response2.id,
                                                          amount=400)

        TransferAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Max910', password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(transfer_account_request)










