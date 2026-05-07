from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.credit_request_requester import CreditRequestRequester
from src.main.api.requests.credit_repay_requester import CreditRepayRequester
@pytest.mark.api
class TestRepayCredit:
    def test_repay_credit_valid(self):
        create_user_request = CreateUserRequest(username='Max903', password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Max903', password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        credit_request_request = CreditRequestRequest(accountId=response.id, amount=5000, termMonths=12)

        response = CreditRequestRequester(
            request_spec=RequestSpecs.auth_headers(username='Max903', password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request_request)
        assert response.balance == 5000


        credit_repay_requests=CreditRepayRequest(creditId=response.creditId, accountId=response.id, amount=5000)

        response = CreditRepayRequester(
            request_spec=RequestSpecs.auth_headers(username='Max903', password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(credit_repay_requests)

        assert response.amountDeposited == 5000
    def test_repay_credit_invalid(self):
        create_user_request = CreateUserRequest(username='Max904', password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Max904', password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        credit_request_request = CreditRequestRequest(accountId=response.id, amount=5000, termMonths=12)

        response = CreditRequestRequester(
            request_spec=RequestSpecs.auth_headers(username='Max904', password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request_request)
        assert response.balance == 5000

        credit_repay_requests = CreditRepayRequest(creditId=response.creditId, accountId=response.id, amount=6000)

        CreditRepayRequester(
            request_spec=RequestSpecs.auth_headers(username='Max904', password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_unprocessable()
        ).post(credit_repay_requests)



