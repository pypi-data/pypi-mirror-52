from sauronmodels.account.owner_type import Owner_type
from sauronmodels.utils.currency import Currency


class Account:

    def __init__(self,
                 id: int,
                 owner_id: int,
                 owner_type: Owner_type,
                 currency: Currency,
                 current_balance: float,
                 credit_balance: float,
                 activated: bool):
        self.__id = id
        self.__owner_id = owner_id
        self.__owner_type = owner_type
        self.__currency = currency
        self.__current_balance = current_balance
        self.__credit_balance = credit_balance
        self.__activated = activated

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        self.__id = value

    @property
    def owner_id(self) -> int:
        return self.owner_id

    @owner_id.setter
    def owner_id(self, value: int):
        self.owner_id = value

    @property
    def owner_type(self) -> Owner_type:
        return self.__owner_type

    @owner_type.setter
    def owner_type(self, value: Owner_type):
        self.__owner_type = value

    @property
    def currency(self) -> Currency:
        return self.__currency

    @currency.setter
    def currency(self, value: Currency):
        self.__currency = value

    @property
    def current_balance(self) -> float:
        return self.__current_balance

    @current_balance.setter
    def current_balance(self, value: float):
        self.__current_balance = value

    @property
    def credit_balance(self) -> float:
        return self.__credit_balance

    @credit_balance.setter
    def credit_balance(self, value: float):
        self.__credit_balance = value

    @property
    def activated(self) -> bool:
        return self.__activated

    @activated.setter
    def activated(self, value: bool):
        self.__activated = value
