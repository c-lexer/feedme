from datetime import datetime

import requests
from bs4 import BeautifulSoup


wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]


class Kurve:
    def __init__(self):
        self.url = "https://www.felsen-keller.at/"

    def get_menus(self, wochentag=None) -> dict:
        kurve_page = requests.get(
            self.url,
            timeout=50,
        )
        soup = BeautifulSoup(kurve_page.text, "html.parser")

        data = {}
        for menu in soup.find_all("div", class_="tagesmenues_content"):
            wochentag = wochentage[
                datetime.strptime(menu.p.string, "%d.%m.%Y").weekday()
            ]
            data[wochentag] = menu.p.find_next_siblings()

        daily_menus = {}
        for menu in data.items():
            menustr = ""
            menus = []
            for line in menu[1][1:]:
                if "Menü" in line.string:
                    menus.append(menustr)
                    menustr = ""
                else:
                    menustr += line.string + "\n"
            menus.append(menustr)
            daily_menus[menu[0]] = menus

        return daily_menus
