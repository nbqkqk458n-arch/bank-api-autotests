import pytest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from sqlalchemy.orm import  Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest

@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self, db_session: Session, api_manager: ApiManager, create_user_request:CreateUserRequest, deposit_account_request:DepositAccountRequest):
        response = api_manager.user_steps.deposit_account(deposit_account_request, create_user_request)
        assert response.balance == 1000
        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.balance == response.balance, 'Счет не пополнен,изменения баланса не сохранилось в базе'




    def test_deposit_account_invalid(self, db_session: Session, api_manager: ApiManager,create_user_request: CreateUserRequest, deposit_account_request_invalid:DepositAccountRequest):
        account_before = Account.get_account_by_id(db_session,deposit_account_request_invalid.accountId)
        api_manager.user_steps.deposit_account_invalid(deposit_account_request_invalid, create_user_request)
        account_after = Account.get_account_by_id(db_session, deposit_account_request_invalid.accountId)
        assert account_before.balance == account_after.balance, 'Счет пополнен,изменения баланса в базе сохранены'










