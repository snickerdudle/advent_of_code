# Make a folder named "day_xx" where xx is the number of the day. In that
# folder, make a file named "day_xx.txt" and paste the puzzle input into it.
# Then, create a file named "day_xx.py" and paste template code into it.

import sys
import requests
import os
from pathlib import Path
import datetime


SESSION_ID = os.environ["AOC_SESSION_ID"]
current_year = datetime.datetime.now().year

if not SESSION_ID:
    raise ValueError("Session ID is not found in the envvars!")


def getPuzzleForDayX(day: int):
    # Go to the webpage and download the puzzle input into a variable
    url = f"https://adventofcode.com/{current_year}/day/{day}/input"
    page_content = requests.get(url, cookies={"session": SESSION_ID}).text
    return page_content


if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print("Usage: python make_new_day.py <day>")
        sys.exit(1)

    day = sys.argv[1]
    page_content = getPuzzleForDayX(int(day))
    cur_path = Path(__file__).resolve().parent
    day_path = cur_path / f"{current_year}" / f"day_{day}"
    day_path.mkdir(exist_ok=True)

    if not (day_path / f"day_{day}.txt").exists():
        with open(day_path / f"day_{day}.txt", "w") as f:
            f.write(page_content)
        print('Created file "day_{day}.txt" with puzzle input.'.format(day=day))

    if not (day_path / f"day_{day}.py").exists():
        with open(day_path / f"day_{day}.py", "w") as f:
            with open(cur_path / "blank.py", "r") as blank:
                f.write(blank.read().replace("XXX", day))
        print('Created file "day_{day}.py" with template code.'.format(day=day))
