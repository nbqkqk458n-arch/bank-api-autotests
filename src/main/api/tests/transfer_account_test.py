import pytest
from src.main.api.db.crud.transaction_crud import TransferCrudDb as Transfer
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest

@pytest.mark.api
class TestTransferAccount:
    def test_transfer_account_valid(self,db_session:Session, api_manager:ApiManager, create_user_request:CreateUserRequest,transfer_account_request:TransferAccountRequest):
        response = api_manager.user_steps.transfer_account(create_user_request,transfer_account_request)
        assert response.fromAccountIdBalance == 500
        transfer_from_db = Transfer.get_transfer_by_data(db_session, transfer_account_request.toAccountId,transfer_account_request.fromAccountId,transfer_account_request.amount)
        assert transfer_from_db.from_account_id==response.fromAccountId, 'Не совпадают аккаунты списания'
        assert transfer_from_db.amount ==transfer_account_request.amount, 'Не совпадают суммы переводов'


    def test_transfer_account_invalid(self,db_session:Session, api_manager:ApiManager, create_user_request:CreateUserRequest,transfer_account_request_invalid:TransferAccountRequest):
        api_manager.user_steps.transfer_account_invalid(create_user_request,transfer_account_request_invalid)
        transfer_from_db = Transfer.get_transfer_by_data(db_session, transfer_account_request_invalid.toAccountId,transfer_account_request_invalid.fromAccountId,transfer_account_request_invalid.amount)
        assert transfer_from_db is None, 'Перевод осуществлен'












