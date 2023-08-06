
class Fee:
    def __init__(self,
                 id: int,
                 name: str,
                 amount: float,
                 ):
        self.__id = id
        self.__name = name
        self.__amount = amount

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        self.__id = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def amount(self) -> float:
        return self.__amount

    @amount.setter
    def amount(self, value: float):
        self.__amount = value
