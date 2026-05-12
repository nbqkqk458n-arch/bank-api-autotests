from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transfer


class TransferCrudDb:
    @staticmethod
    def get_transfer_by_data(db: Session, to_account_id: int, from_account_id:int, amount:float)->Transfer|None:
        return db.query(Transfer).filter_by(to_account_id=to_account_id, from_account_id=from_account_id, amount=amount).first()
    @staticmethod
    def transfer_account(db: Session, toAccountId: int, fromAccountId: int, amount: float):
        transfer=Transfer(
            toAccountId=toAccountId,
            fromAccountId=fromAccountId,
            amount=amount
        )
        db.commit()
        db.refresh(transfer)
        return transfer

