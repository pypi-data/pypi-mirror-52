from sauronmodels.account.owner_type import Owner_type
from sauronmodels.utils.currency import Currency
from typing import Optional


class Account:
    def __init__(self,
                 owner_id: int,
                 owner_type: Owner_type,
                 id: Optional[int] = None,
                 currency: Optional[Currency] = None,
                 current_balance: Optional[float] = None,
                 credit_balance: Optional[float] = None,
                 activated: Optional[bool] = None):
        self.__id = id
        self.__owner_id = owner_id
        self.__owner_type = owner_type
        self.__currency = currency
        self.__current_balance = current_balance
        self.__credit_balance = credit_balance
        self.__activated = activated


    @property
    def id(self) -> Optional[int]:
        return self.__id

    @id.setter
    def id(self, value: Optional[int]):
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
    def currency(self) -> Optional[Currency]:
        return self.__currency

    @currency.setter
    def currency(self, value: Optional[Currency]):
        self.__currency = value

    @property
    def current_balance(self) -> Optional[float]:
        return self.__current_balance

    @current_balance.setter
    def current_balance(self, value: Optional[float]):
        self.__current_balance = value

    @property
    def credit_balance(self) -> Optional[float]:
        return self.__credit_balance

    @credit_balance.setter
    def credit_balance(self, value: Optional[float]):
        self.__credit_balance = value

    @property
    def activated(self) -> Optional[bool]:
        return self.__activated

    @activated.setter
    def activated(self, value: Optional[bool]):
        self.__activated = value
