from src.main.api.models.base_model import BaseModel


class CreditRequestResponse(BaseModel):
    id: int
    amount: int
    balance: float
    creditId: int        #Модель скорректирована под реальный ответ API, баг, возвращает id вместо accountId
                        #И не возвращает поле termMonth как указано в спецификации