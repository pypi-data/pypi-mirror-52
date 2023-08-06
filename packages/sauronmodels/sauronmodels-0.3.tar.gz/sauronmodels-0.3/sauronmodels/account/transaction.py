import datetime
from sauronmodels.account.account import Account
from sauronmodels.account.concept import Concept
from sauronmodels.account.fee import Fee
from sauronmodels.account.impost import Tax
from sauronmodels.account.status import Status
from sauronmodels.account.type import Type
from typing import List,Optional

class Transaction:

    def __init__(self,
                 type: Type,
                 concept: Concept,
                 description: str,
                 external_ref: str,
                 equivalent_usd: float,
                 convertion_rate: float,
                 base: float,
                 account: Account,
                 id: Optional[int] = None,
                 partial_balance: Optional[float] = None,
                 created: Optional[datetime.datetime] = None,
                 status: Optional[Status] = None,
                 currency: Optional[str] = None,
                 taxes: Optional[List[Tax]] = None,
                 fees: Optional[List[Fee]] = None
                 ):
        self.__id = id
        self.__partial_balance = partial_balance
        self.__created = created
        self.__type = type
        self.__concept = concept
        self.__description = description
        self.__external_ref = external_ref
        self.__status = status
        self.__base = base
        self.__equivalent_usd = equivalent_usd
        self.__convertion_rate = convertion_rate
        self.__currency = currency
        self.__account = account
        self.__taxes = taxes
        self.__fees = fees

    @property
    def id(self) -> Optional[int]:
        return self.__id

    @id.setter
    def id(self, value: Optional[int]):
        self.__id = value

    @property
    def currency(self) -> Optional[str]:
        return self.__currency

    @currency.setter
    def currency(self, value: Optional[str]):
        self.__currency = value

    @property
    def partial_balance(self) -> Optional[float]:
        return self.__partial_balance

    @partial_balance.setter
    def partial_balance(self, value: Optional[float]):
        self.__partial_balance = value

    @property
    def created(self) -> Optional[datetime.datetime]:
        return self.__created

    @created.setter
    def created(self, value: Optional[datetime.datetime]):
        self.__created = value

    @property
    def type(self) -> Type:
        return self.__type

    @type.setter
    def type(self, value: Type):
        self.__type = value

    @property
    def concept(self) -> Concept:
        return self.__concept

    @concept.setter
    def concept(self, value: Concept):
        self.__concept = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value

    @property
    def external_ref(self) -> str:
        return self.__external_ref

    @external_ref.setter
    def external_ref(self, value: str):
        self.__external_ref = value

    @property
    def status(self) -> Optional[Status]:
        return self.__status

    @status.setter
    def status(self, value: Optional[Status]):
        self.__status = value

    @property
    def base(self) -> float:
        return self.__base

    @base.setter
    def base(self, value: float):
        self.__base = value

    @property
    def equivalent_usd(self) -> float:
        return self.__equivalent_usd

    @equivalent_usd.setter
    def equivalent_usd(self, value: float):
        self.__equivalent_usd = value

    @property
    def convertion_rate(self) -> float:
        return self.__convertion_rate

    @convertion_rate.setter
    def convertion_rate(self, value: float):
        self.__convertion_rate = value

    @property
    def account(self) -> Account:
        return self.__account

    @account.setter
    def account(self, value: Account):
        self.__account = value

    @property
    def taxes(self) -> Optional[List[Tax]]:
        return self.__taxes

    @taxes.setter
    def taxes(self, value: Optional[List[Tax]]):
        self.__taxes = value

    @property
    def fees(self) -> Optional[List[Fee]]:
        return self.__fees

    @fees.setter
    def fees(self, value: Optional[List[Fee]]):
        self.__fees = value
