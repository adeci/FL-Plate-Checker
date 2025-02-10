# Florida License Plate Availability Checker

This program will fetch all available **custom Florida license plate** combos with a given X length (1-3) by querying the Florida DMV website.

![example](/example.png)

## Installation

Install **Python 3.7+**

Then create a venv to run this with:

```sh
python3 -m venv env

source env/bin/activate
# or env\Scripts\activate for Windows
```

Then install all the dependencies with:

```sh
pip install -r requirements.txt
```

## Usage

Simply run:

```sh
python plate_checker.py
```

At this point a TUI selection menu will appear to choose the plate combo you want, and the script will iterate through all possible combos using 5 group batches. The available plates will be printed as they are found and appended to available_plates.txt

## Notes

This is for **educational purposes only** and is not affiliated with or approved of by the Florida DMV in any way. Use at your own risk.

As of 2/10/25 there are **9.8k+** 3 letter plate combos available, and **0** 1/2 letter plate combos available.
