"""Day 15."""
from pathlib import Path


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_15.txt", "r") as f:
        raw_data = f.read().strip().split(",")

    return raw_data


def custom_hash(data):
    cur = 0

    for c in data:
        cur += ord(c)
        cur *= 17
        cur %= 256

    return cur


def part_1():
    raw_data = get_data()
    result_sum = 0

    for s in raw_data:
        print(custom_hash(s[:2]))
        result_sum += custom_hash(s)

    print(result_sum)


class Lens:
    def __init__(self, name, value, previous=None, next=None):
        self.name = name
        self.value = value
        self.previous = previous
        self.next = next

    def insertNext(self, name, value):
        if self.next is None:
            self.next = Lens(name, value, self)
        else:
            if self.next.name == name:
                self.next.value = value
            else:
                self.next.insertNext(name, value)

    def insertNextLens(self, lens):
        if self.next is None:
            self.next = lens
            lens.previous = self
        else:
            if self.next.name == lens.name:
                self.next.removeSelf()
                lens.next = self.next
                lens.previous = self
                self.next = lens
            else:
                self.next.insertNextLens(lens)

    def removeSelf(self):
        if self.previous is not None:
            self.previous.next = self.next
        if self.next is not None:
            self.next.previous = self.previous


class HashMap:
    def __init__(self):
        self.lenses = {i: None for i in range(256)}
        self.hashmap = {}

    def process(self, data):
        if "-" in data:
            name, value = data[:-1], None
            self.remove(name)
        else:
            name, value = data.split("=")
            value = int(value)
            self.insert(name, value)

    def insert(self, name, value):
        index = custom_hash(name)
        if name in self.hashmap:
            self.hashmap[name].value = value
            return
        new_lens = Lens(name, value)
        if self.lenses[index] is None:
            self.lenses[index] = new_lens
        else:
            self.lenses[index].insertNextLens(new_lens)

        self.hashmap[name] = new_lens

    def remove(self, name):
        index = custom_hash(name)
        if name not in self.hashmap:
            return
        else:
            self.hashmap[name].removeSelf()
            if self.lenses[index].name == name:
                self.lenses[index] = self.hashmap[name].next
            del self.hashmap[name]

    def printBins(self):
        for bin_idx in range(256):
            if self.lenses[bin_idx] is None:
                continue
            cur_lens = self.lenses[bin_idx]
            print(bin_idx, end=": ")
            while cur_lens is not None:
                print(f"[{cur_lens.name}:{cur_lens.value}] ", end="")
                cur_lens = cur_lens.next
            print()

    def getAllPowerSum(self):
        total_result = 0
        for bin_idx in range(256):
            if self.lenses[bin_idx] is None:
                continue
            cur_lens = self.lenses[bin_idx]
            cur_order = 1
            while cur_lens is not None:
                this_result = bin_idx + 1
                this_result *= cur_order
                this_result *= cur_lens.value
                total_result += this_result
                cur_order += 1
                cur_lens = cur_lens.next
        return total_result


def part_2():
    hm = HashMap()
    raw_data = get_data()

    for s in raw_data:
        hm.process(s)
        # print(s)
        # hm.printBins()

    # hm.printBins()
    print(hm.getAllPowerSum())


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
