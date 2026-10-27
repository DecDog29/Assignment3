"""Reusable console helpers: validated prompts and menus."""
from collections.abc import Callable
from typing import TypeVar

from yowd.validation import ValidationError

T = TypeVar("T")


def ask(label: str, validator: Callable[[str], T]) -> T:
    """Prompt until ``validator`` accepts the input.

    Each prompt names the field, and validation errors are shown inline
    (Assignment 1 usability requirement: clear labels and feedback).
    """
    while True:
        raw = input(f"{label}: ")
        try:
            return validator(raw)
        except ValidationError as error:
            print(f"  ! {error}")


def confirm(question: str) -> bool:
    """Ask a yes/no question."""
    while True:
        answer = input(f"{question} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  ! Please answer y or n.")


def run_menu(
    title: str, options: list[tuple[str, Callable[[], None]]]
) -> None:
    """Show a numbered menu until the user picks 0 (Back/Exit)."""
    while True:
        print(f"\n=== {title} ===")
        for number, (text, _) in enumerate(options, start=1):
            print(f"  {number}. {text}")
        print("  0. Back / Exit")
        choice = input("Select an option: ").strip()
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            options[int(choice) - 1][1]()
        else:
            print("  ! Invalid option, please enter a number from the menu.")
