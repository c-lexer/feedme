import os
import json
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
import fitz


wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]


class Krall:
    def __init__(self):
        self.url = "https://www.gasthof-krall.at/"
        self.pdf_name = "Menu.pdf"

    def get_menus(self, wochentag=None) -> dict:
        if self.get_pdf():
            content = self.parse_contents()
            if wochentag:
                return content[wochentag]
            return content

    def get_pdf(self) -> bool:
        krall_page = requests.get(
            self.url,
            timeout=50,
        )

        soup = BeautifulSoup(krall_page.text, "html.parser")

        for link in soup.find_all("div", class_="leftDownload"):
            if "Wochenmen" in (link.a.get("href")):
                response = requests.get(
                    self.url + link.a.get("href"),
                    timeout=50,
                )
                with open(self.pdf_name, "wb") as f:
                    f.write(response.content)

        return os.path.exists(self.pdf_name)

    def parse_contents(self) -> dict:
        parsed_pdf = fitz.open(self.pdf_name)
        text = parsed_pdf.load_page(0).get_text("json")
        json_content = json.loads(text)

        menu1 = defaultdict(str)
        menu2 = defaultdict(str)

        day_iterator = -1

        for block in json_content["blocks"]:
            if block["lines"][0]["spans"][0]["text"] in wochentage:
                day_iterator += 1
            if len(block["lines"]) == 3:
                menu1[wochentage[day_iterator]] += (
                    "\n" + block["lines"][1]["spans"][0]["text"]
                )
                menu2[wochentage[day_iterator]] += (
                    "\n" + block["lines"][2]["spans"][0]["text"]
                )
            if (
                len(block["lines"]) == 2
                and "*" not in block["lines"][0]["spans"][0]["text"]
                and "*" not in block["lines"][1]["spans"][0]["text"]
                and "Men" not in block["lines"][0]["spans"][0]["text"]
                and "Men" not in block["lines"][1]["spans"][0]["text"]
            ):
                menu1[wochentage[day_iterator]] += (
                    "\n" + block["lines"][0]["spans"][0]["text"]
                )
                menu2[wochentage[day_iterator]] += (
                    "\n" + block["lines"][1]["spans"][0]["text"]
                )

        data = {}
        for tag in wochentage:
            data[tag] = [menu1[tag][1:], menu2[tag][1:]]  # remove first linebreak

        return data

    def __del__(self):
        if os.path.exists("Krall.pdf"):
            os.remove("Krall.pdf")
