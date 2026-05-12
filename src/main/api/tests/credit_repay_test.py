import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.classes.api_manager import ApiManager
from sqlalchemy.orm import Session

@pytest.mark.api
class TestRepayCredit:
    def test_repay_credit_valid(self,db_session: Session, api_manager: ApiManager, create_secret_user_request:CreateUserRequest, credit_repay_request:CreditRepayRequest):
        response = api_manager.user_steps.credit_repay_request(create_secret_user_request, credit_repay_request)
        assert response.amountDeposited == 5000
        credit = Credit.get_credit_by_id(db_session, response.creditId)
        assert credit.balance == 0, 'Кредит не погашен, в БД долг'
    def test_repay_credit_invalid(self,db_session:Session, api_manager: ApiManager, create_secret_user_request:CreateUserRequest, credit_repay_request_invalid:CreditRepayRequest):
        api_manager.user_steps.credit_repay_request_invalid(create_secret_user_request, credit_repay_request_invalid)
        credit = Credit.get_credit_by_id(db_session, credit_repay_request_invalid.creditId)
        assert credit.balance == -5000, 'Кредит погашен, в БД долг отсутствует'



