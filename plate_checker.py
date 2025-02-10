import curses
import requests
from itertools import product
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
import shutil
import pyfiglet


def get_terminal_size():
    size = shutil.get_terminal_size((80, 24))
    return size.columns, size.lines


def draw_menu(stdscr, selected):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    options = ["[ 1-Letter Combo Search ]",
               "[ 2-Letter Combo Search ]", "[ 3-Letter Combo Search ]"]
    title = "Choose an Option"

    start_y = height // 2 - len(options) // 2
    start_x = width // 2

    stdscr.addstr(start_y - 2, start_x - len(title) // 2, title, curses.A_BOLD)

    for i, option in enumerate(options):
        x = start_x - len(option) // 2
        if i == selected:
            stdscr.addstr(start_y + i, x, f"> {option} <", curses.A_REVERSE)
        else:
            stdscr.addstr(start_y + i, x, option)

    stdscr.refresh()


def menu_select(stdscr):
    """Handles user input for selecting an option."""
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    selected = 0
    options = ["1", "2", "3"]

    while True:
        draw_menu(stdscr, selected)
        key = stdscr.getch()

        if key in [curses.KEY_UP, ord('w'), ord('k')]:
            selected = max(0, selected - 1)
        elif key in [curses.KEY_DOWN, ord('s'), ord('j')]:
            selected = min(len(options) - 1, selected + 1)
        elif key in [curses.KEY_ENTER, ord('\n')]:
            return options[selected]


def display_ascii_banner(text):
    os.system("cls" if os.name == "nt" else "clear")
    banner = pyfiglet.figlet_format(
        text, font="slant")
    print(banner)


def get_form_values():
    url = 'https://services.flhsmv.gov/mvcheckpersonalplate/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    return {
        '__VIEWSTATE': soup.find("input", {"id": "__VIEWSTATE"})['value'],
        '__VIEWSTATEGENERATOR': soup.find("input", {"id": "__VIEWSTATEGENERATOR"})['value'],
        '__EVENTVALIDATION': soup.find("input", {"id": "__EVENTVALIDATION"})['value'],
        'ctl00$MainContent$btnSubmit': 'Submit'
    }


def save_progress(filename, available_plates):
    with open(filename, "a") as f:
        for plate in available_plates:
            f.write(f"{plate}\n")


def check_all_combinations(combination_length):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    combinations = ["".join(p) for p in product(
        letters, repeat=combination_length)]
    total_combinations = len(combinations)
    batch_size = 5
    correlation = ["One", "Two", "Three", "Four", "Five"]

    print(f"Total plate combinations to check: {total_combinations}")

    with tqdm(total=total_combinations, desc="Checking Plates", dynamic_ncols=True, position=0, leave=True) as pbar:
        for i in range(0, total_combinations, batch_size):
            batch = combinations[i:i + batch_size]
            formValues = get_form_values()

            for index, plate in enumerate(batch):
                formValues[f'ctl00$MainContent$txtInputRow{correlation[index]}'] = plate

            response = requests.post(
                'https://services.flhsmv.gov/mvcheckpersonalplate/', data=formValues)
            html_text = response.text
            soup = BeautifulSoup(html_text, 'html.parser')

            hits = []
            for index, plate in enumerate(batch):
                availability_span = soup.find(
                    "span", {"id": f"MainContent_lblOutPutRow{correlation[index]}"})
                if availability_span and availability_span.text.strip().upper() == "AVAILABLE":
                    hits.append(plate)

            tqdm.write(f"Currently checking: {', '.join(batch)}")

            if hits:
                tqdm.write(f"AVAILABLE: {', '.join(hits)}")
                save_progress("available_plates.txt", hits)

            pbar.update(len(batch))

    print("\nScanning complete. Results saved incrementally to available_plates.txt")


if __name__ == "__main__":
    choice = curses.wrapper(menu_select)

    if choice == '1':
        display_ascii_banner("1-Letter Combo")
        check_all_combinations(1)
    if choice == '2':
        display_ascii_banner("2-Letter Combo")
        check_all_combinations(2)
    elif choice == '3':
        display_ascii_banner("3-Letter Combo")
        check_all_combinations(3)
