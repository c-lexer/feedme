from datetime import datetime

import requests
from bs4 import BeautifulSoup


wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]


class Karli:
    def __init__(self):
        self.url = "https://www.karlis-gasthaus.at/speisen/"

    def contains_number(self, s):
        if s:
            return any(c.isdigit() for c in s) or "€" in s
        return False

    def get_menus(self, wochentag=None) -> dict:
        data = {}
        for tag in wochentage:
            url = self.url + tag.lower()
            karli_page = requests.get(
                url,
                timeout=50,
            )
            soup = BeautifulSoup(karli_page.text, "html.parser")
            for menu in soup.find_all(
                "span", attrs={"style": "font-family:libre baskerville,serif;"}
            ):
                if menu.string in wochentage:
                    data[menu.string] = [
                        "Tagessuppe  -  Wienerschnitzel mit Beilage nach Wahl und gem. Salat"
                    ]
                if (
                    menu.string
                    and menu.string not in wochentage
                    and not self.contains_number(menu.string)
                    and "Wienerschnitzel" not in menu.string
                ):
                    data[tag].append(menu.string)

        return data
