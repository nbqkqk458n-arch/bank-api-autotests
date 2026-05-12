import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.create_user_request import CreateSecretUserRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest

@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_secret_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateSecretUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def deposit_account_request(api_manager,create_user_request):
    account = api_manager.user_steps.create_account(create_user_request)
    return DepositAccountRequest(accountId=account.id, amount = 1000)
@pytest.fixture
def deposit_account_request_invalid(api_manager,create_user_request):
    account = api_manager.user_steps.create_account(create_user_request)
    return DepositAccountRequest(accountId=account.id, amount = 999)
@pytest.fixture
def transfer_account_request(api_manager,create_user_request):
    account1 = api_manager.user_steps.create_account(create_user_request)
    account2 = api_manager.user_steps.create_account(create_user_request)
    api_manager.user_steps.deposit_account(DepositAccountRequest(accountId=account1.id, amount=1000), create_user_request)
    return TransferAccountRequest(fromAccountId=account1.id, toAccountId=account2.id, amount=500)

@pytest.fixture
def transfer_account_request_invalid(api_manager,create_user_request):
    account1 = api_manager.user_steps.create_account(create_user_request)
    account2 = api_manager.user_steps.create_account(create_user_request)
    api_manager.user_steps.deposit_account(DepositAccountRequest(accountId=account1.id, amount=1000), create_user_request)
    return TransferAccountRequest(fromAccountId=account1.id, toAccountId=account2.id, amount=400)
@pytest.fixture
def credit_request_request(api_manager,create_secret_user_request):
    account=api_manager.user_steps.create_account(create_secret_user_request)
    return CreditRequestRequest(accountId=account.id, amount = 5000, termMonths= 12)

@pytest.fixture
def credit_request_request_invalid(api_manager,create_secret_user_request):
    account=api_manager.user_steps.create_account(create_secret_user_request)
    return CreditRequestRequest(accountId=account.id, amount = 16000, termMonths= 12)

@pytest.fixture
def credit_repay_request(api_manager, create_secret_user_request):
    account = api_manager.user_steps.create_account(create_secret_user_request)
    credit_response = CreditRequestRequest(accountId=account.id, amount = 5000, termMonths= 12)
    credit = api_manager.user_steps.credit_request_request(create_secret_user_request,credit_response)
    return CreditRepayRequest(creditId=credit.creditId, accountId=account.id, amount=5000)

@pytest.fixture
def credit_repay_request_invalid(api_manager, create_secret_user_request):
    account = api_manager.user_steps.create_account(create_secret_user_request)
    credit_request = CreditRequestRequest(accountId=account.id, amount=5000, termMonths=12)
    credit = api_manager.user_steps.credit_request_request(create_secret_user_request, credit_request)
    assert credit.balance == 5000, f'Баланс кредита после создания {credit.balance}'
    return CreditRepayRequest(creditId=credit.creditId, accountId=account.id, amount=6000)







