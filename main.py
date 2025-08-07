"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Marie Koblizkova
email: mariekoblizkova@seznam.cz
"""

# prikaz_pro_spusteni = py main.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6104' vysledky_trebic.csv

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv


def zadej_argumenty(): 
    if len(sys.argv) != 3:
        print("Chyba: Skript vyžaduje 2 argumenty:")
        print("Použití: python vysledky_scraper.py <URL> <vystup.csv>")
        sys.exit(1)

    url = sys.argv[1]
    if not url.startswith("https://www.volby.cz/pls/ps2017nss/"):
        print("Chybný odkaz. Zkontroluj, zda odkazuješ na platnou stránku voleb 2017.")
        sys.exit(1)

    return url, sys.argv[2]


def stahni_html(url):
    odpoved = requests.get(url)
    if odpoved.status_code != 200:
        print(f"Chyba při načítání stránky ({odpoved.status_code}): {url}")
        sys.exit(1)
    return BeautifulSoup(odpoved.text, "html.parser")


def ziskej_odkazy_obci(soup, zakladni_url):
    obce = []
    radky = soup.find_all("tr")
    for radek in radky:
        bunky = radek.find_all("td")
        if len(bunky) >= 3:
            bunka_kod = bunky[0].find("a")
            if bunka_kod:
                kod = bunka_kod.text.strip()
                nazev = bunky[1].text.strip()
                detail_url = urljoin(zakladni_url, bunka_kod["href"])
                obce.append((kod, nazev, detail_url))
    return obce


def ziskej_cislo(soup, hlavicka_id):
    bunka = soup.find("td", headers=hlavicka_id)
    if bunka:
        return bunka.text.strip().replace('\xa0', '').replace(' ', '')
    return '0'


def ziskej_hlasy_stran(soup):
    strany = {}
    tabulky = soup.find_all("table")
    for tabulka in tabulky:
        radky = tabulka.find_all("tr")
        for radek in radky:
            bunky = radek.find_all("td")
            if len(bunky) == 5:
                nazev_strany = bunky[1].text.strip()
                hlasy = bunky[2].text.strip().replace('\xa0', '').replace(' ', '')
                strany[nazev_strany] = hlasy
    return strany


def ziskej_data_obce(kod, nazev, url):
    soup = stahni_html(url)
    registrovani = ziskej_cislo(soup, "sa2")
    obalky = ziskej_cislo(soup, "sa3")
    platne = ziskej_cislo(soup, "sa6")
    hlasy_stran = ziskej_hlasy_stran(soup)
    return {
        "kod": kod,
        "obec": nazev,
        "registrovani": registrovani,
        "obalky": obalky,
        "platne": platne,
        **hlasy_stran
    }


def main():
    url, vystupni_soubor = zadej_argumenty()

    print(f"STAHUJI DATA Z VYBRANÉ URL: {url}")

    zakladni_url = url.rsplit("/", 1)[0] + "/"
    soup = stahni_html(url)
    obce = ziskej_odkazy_obci(soup, zakladni_url)

    vsechna_data = []
    vsechny_strany = set()

    for kod, nazev, detail_url in obce:
        data = ziskej_data_obce(kod, nazev, detail_url)
        vsechny_strany.update(data.keys() - {"kod", "obec", "registrovani", "obalky", "platne"})
        vsechna_data.append(data)

    serazene_strany = sorted(vsechny_strany)
    hlavicky = ["kod", "obec", "registrovani", "obalky", "platne"] + serazene_strany

    with open(vystupni_soubor, mode="w", newline="", encoding="utf-8-sig") as f:
        zapisovac = csv.DictWriter(f, fieldnames=hlavicky, delimiter=';')
        zapisovac.writeheader()
        for radek in vsechna_data:
            for strana in serazene_strany:
                radek.setdefault(strana, "0")
            zapisovac.writerow(radek)

    print(f"VÝSLEDKY ULOŽENY DO: {vystupni_soubor}")
    print("Ukončuji program.")


if __name__ == "__main__":
    main()
