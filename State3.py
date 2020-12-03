from __future__ import annotations
from abc import ABC, abstractmethod
import random

class GumballMashine(ABC):
    _state = None
    count = 0

    def __init__(self, numberGumballs) -> None:
        self.set_state(NoQuarterState)
        self.count = numberGumballs

    def set_state(self, state: State):
        print(f"Переходим в состояние: {state.toString(self)}")
        self._state = state

    def insertQuarter(self):
        self._state.insertQuarter(self)

    def ejectQuarter(self):
        self._state.ejectQuarter(self)

    def turnCrank(self):
        self._state.turnCrank(self)
        self._state.dispense(self)

    def releaseBall(self):
        print("Шарик катится к выходу")
        if self.count != 0:
            self.count = self.count - 1

    def getCount(self) -> int:
        return self.count

    def refill(self, c):
        self.count = c
        self.set_state(NoQuarterState)

    def toString(self) -> str:
        result = "\n----------------------------------\n"
        result = result + "Mighty Gumball, Inc.\n"
        result = result + f"Запас: {self.count}\n"
        result = result + f"Состояние: {self._state.toString(self)}\n\n"
        return result

class State(ABC):
    _context = None

    @property
    def context(self) -> GumballMashine:
        return self._context

    @context.setter
    def context(self, context: GumballMashine) -> None:
        self._context = context

    @abstractmethod
    def insertQuarter(self) -> None:
        pass

    @abstractmethod
    def ejectQuarter(self) -> None:
        pass

    @abstractmethod
    def turnCrank(self) -> None:
        pass

    @abstractmethod
    def dispense(self) -> None:
        pass

    @abstractmethod
    def toString(self) -> str:
        pass

class NoQuarterState(State):
    def insertQuarter(self) -> None:
        print("Вы вставили монету")
        self.set_state(HasQuarterState)

    def ejectQuarter(self) -> None:
        print("Вы не вставили монету")

    def turnCrank(self) -> None:
        print("Вы дернули рычаг, но монеты нет")

    def dispense(self) -> None:
        print("Сначало нужно заплатить")

    def toString(self) -> str:
        return "Ожидание монеты"
class SoldOutState(State):
    def insertQuarter(self) -> None:
        print("Вы не можете вставить монету, автомат пуст")

    def ejectQuarter(self) -> None:
        print("Вы не можете извлечь монету, вы её не вставили")

    def turnCrank(self) -> None:
        print("Вы повернули рычаг, но автомат пуст")

    def dispense(self) -> None:
        print("Автомат пуст")

    def toString(self) -> str:
        return "Автомат пуст"

class HasQuarterState(State):
    def insertQuarter(self) -> None:
        print("Вы не можете вставить ещё одне монету")

    def ejectQuarter(self) -> None:
        print("Монета возвращена")
        self.set_state(NoQuarterState)

    def turnCrank(self) -> None:
        print("Вы повернули рычаг...")
        winner = random.randint(0,1)
        if winner == 0 and self.getCount() > 0:
            self.set_state(WinnerState)
        else:
            self.set_state(SoldState)

    def dispense(self) -> None:
        print("Шарик не может быть выдан")

    def toString(self) -> str:
        return "Ожидание поворота рычага"

class SoldState(State):
    def insertQuarter(self) -> None:
        print("Подождите, вы уже получили жвачку")

    def ejectQuarter(self) -> None:
        print("Извините, вы уже дернули за рычаг")

    def turnCrank(self) -> None:
        print("Поворачивать второй раз - бессмысленно")

    def dispense(self) -> None:
        self.releaseBall()
        if self.getCount() > 0:
            self.set_state(NoQuarterState)
        else:
            print("Упс, закончились шарики!")
            self.set_state(SoldOutState)

    def toString(self) -> str:
        print("Выдан шарик")

class WinnerState(State):
    def insertQuarter(self) -> None:
        print("Подождите, вы уже получили жвачку")

    def ejectQuarter(self) -> None:
        print("Извините, вы уже дернули з рычаг")

    def turnCrank(self) -> None:
        print("Поворачивать второй раз - бессмысленно")

    def dispense(self) -> None:
        print("Вы выиграли! Вы получите 2 шарика!")
        self.releaseBall()
        if self.getCount() == 0:
            self.set_state(SoldOutState)
        else:
            self.releaseBall()
            if self.getCount() > 0:
                self.set_state(NoQuarterState)
            else:
                print("Упс, автомат пуст!")
                self.set_state(SoldOutState)

    def toString(self) -> str:
        print("Получено 2 шарика, потому что вы победитель!")

def main():
    gumballMashine = GumballMashine(30)

    print(gumballMashine.toString())

    gumballMashine.insertQuarter()
    gumballMashine.turnCrank()
    print("===============")
    gumballMashine.insertQuarter()
    gumballMashine.turnCrank()
    print("===============")
    gumballMashine.insertQuarter()
    gumballMashine.turnCrank()
    print("===============")
    gumballMashine.insertQuarter()
    gumballMashine.turnCrank()

if __name__=="__main__":
    main()

#input() #- для отображения при запуске через файл
