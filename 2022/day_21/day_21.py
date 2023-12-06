"""Day 21."""
from typing import Union, Optional, Type
from functools import cache

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
        self.left = left
        self.right = right
        self.operation = operation

    def get_left_obj(self):
        if self.left is None:
            return None
        return all_monkeys[self.left]

    def get_right_obj(self):
        if self.right is None:
            return None
        return all_monkeys[self.right]

    @property
    def val(self):
        if self._val is None:
            self.update_val()
        return self._val

    def update_val(self):
        if self.left is None:
            raise ValueError(f"No value or left for {self.name}")
        if self.right is None:
            raise ValueError(f"No value or right for {self.name}")
        if self.operation is None:
            raise ValueError(f"No operation for {self.name}")
        op = op_mapping[self.operation]
        self._val = op(all_monkeys[self.left].val, all_monkeys[self.right].val)
        return self._val

    @cache
    def is_human_branch(self):
        if self.name == "humn":
            return True
        if self.left is not None and self.get_left_obj().is_human_branch():
            return True
        if self.right is not None and self.get_right_obj().is_human_branch():
            return True
        return False


def get_data_part_1():
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
    get_data_part_1()
    print(all_monkeys["root"].val)


def part_2():
    human = all_monkeys["humn"]
    cur_root = all_monkeys["root"]

    human_branch, non_human_branch = (
        cur_root.get_left_obj(),
        cur_root.get_right_obj(),
    )
    if human_branch is None or non_human_branch is None:
        raise ValueError("No branches")
    if non_human_branch.is_human_branch():
        human_branch, non_human_branch = non_human_branch, human_branch

    target_val = non_human_branch.val
    cur_root = human_branch

    invert_operations = {
        "-": int.__add__,
        "+": int.__sub__,
        "*": int.__floordiv__,
        "/": int.__mul__,
    }

    while human_branch is not None:
        print(cur_root.name, target_val)
        # Find the next human branch, and invert the opetations that led to
        # the current target_val
        flipped = False
        human_branch, non_human_branch = (
            cur_root.get_left_obj(),
            cur_root.get_right_obj(),
        )
        if human_branch is None or non_human_branch is None:
            break
        if non_human_branch.is_human_branch():
            human_branch, non_human_branch = non_human_branch, human_branch
            flipped = True

        if flipped and cur_root.operation == "-":
            target_val = int.__sub__(non_human_branch.val, target_val)
        elif flipped and cur_root.operation == "/":
            target_val = int.__floordiv__(non_human_branch.val, target_val)
        else:
            inv_op = invert_operations[cur_root.operation]
            target_val = inv_op(target_val, non_human_branch.val)
        cur_root = human_branch

    print(target_val)


if __name__ == "__main__":
    part_1()
    part_2()
