"""Day 21."""
from typing import Union, Optional, Type

MonkeyType = Union[str, Type["Monkey"]]

op_mapping = {
    "+": int.__add__,
    "-": int.__sub__,
    "*": int.__mul__,
    "/": int.__floordiv__,
}

all_monkeys = {}


class Monkey:
    def __init__(
        self,
        name: str,
        val: Optional[int] = None,
        left: Optional[MonkeyType] = None,
        right: Optional[MonkeyType] = None,
        operation: Optional[str] = None,
    ):
        self.name = name
        self._val = val
        self._left = left
        self._right = right
        self._operation = operation

    @property
    def val(self):
        print(self.name)
        if self._val is None:
            self.update_val()
        return self._val

    def update_val(self):
        if self._left is None:
            raise ValueError(f"No value or left for {self.name}")
        if self._right is None:
            raise ValueError(f"No value or right for {self.name}")
        if self._operation is None:
            raise ValueError(f"No operation for {self.name}")
        if isinstance(self._operation, str):
            self._operation = op_mapping[self._operation]
        self._val = self._operation(
            all_monkeys[self._left].val, all_monkeys[self._right].val
        )
        return self._val


def get_data():
    data = open("day_21.txt").read().strip().split("\n")

    for name, content in [line.split(": ") for line in data]:
        if name in all_monkeys:
            raise ValueError(f"Duplicate name {name}")
        if content.isnumeric():
            all_monkeys[name] = Monkey(name, int(content))
        else:
            left, op, right = content.split(" ")
            all_monkeys[name] = Monkey(name, left=left, right=right, operation=op)
    return all_monkeys


def part_1():
    data = get_data()
    print(data)
    print(data["root"].val)


def part_2():
    pass


if __name__ == "__main__":
    part_1()
    part_2()
