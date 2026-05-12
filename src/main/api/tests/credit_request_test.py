import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.classes.api_manager import ApiManager
from sqlalchemy.orm import Session
@pytest.mark.api
class TestCreditRequest:
    def test_credit_request_valid(self, db_session: Session, api_manager: ApiManager, create_secret_user_request: CreateUserRequest, credit_request_request: CreditRequestRequest):
        response = api_manager.user_steps.credit_request_request(create_secret_user_request, credit_request_request)
        assert response.balance == 5000
        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)
        assert credit_from_db.id == response.creditId, 'Кредит отсутствует в базе'
        assert credit_from_db.amount == credit_request_request.amount, 'Cумма кредита не совпадает с БД'



    def test_credit_request_invalid(self,db_session: Session, api_manager: ApiManager, create_secret_user_request: CreateUserRequest, credit_request_request_invalid: CreditRequestRequest):
        api_manager.user_steps.credit_request_request_invalid(create_secret_user_request, credit_request_request_invalid)
        credit_from_db = Credit.get_credit_by_id(db_session,credit_request_request_invalid.accountId)
        assert credit_from_db is None, 'Кредит есть в базе'
# По спецификации должна вернуться 422, баг.

