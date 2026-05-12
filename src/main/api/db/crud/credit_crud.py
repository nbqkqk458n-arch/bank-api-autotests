from sqlalchemy.orm import Session
from src.main.api.db.models.credit_table import Credit

class CreditCrudDb:
    @staticmethod
    def get_credit_by_id(db:Session, account_id:int)->Credit|None:
        return db.query(Credit).filter_by(id=account_id).first()

    @staticmethod
    def request_credit(db: Session, account_id: int, amount: float, termMonths: int )->Credit:
        credit = Credit(
            account_id=account_id,
            amount=amount,
            termMonths=termMonths,
            balance=amount,

        )
        db.add(credit)
        db.commit()
        db.refresh(credit)
        return credit


