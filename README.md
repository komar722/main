Projekt: Elections Scraper

Popis projektu:

Cílem projektu je vytvořit scraper výsledků voleb z roku 2017, který vytáhne data přímo z webu,
ze stránky https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ.


Instalace knihoven:

Do nově vytvořeného vlastního virtuálního prostředí .venv (speciálně pro tento úkol) byly přes příkazový řádek nainstalovány potřebné knihovny třetích stran:

pip install requests

pip install beautifulsoup4.

Pomocí příkazu: pip freeze > requirements.txt  byl vygenerován soubor requirements.txt



Výsledky hlasování za okres Třebíč

Výsledný soubor se spouští pomocí 2 argumentů. První argument obsahuje odkaz, který územní celek chceme scrapovat, druhý argument obsahuje jméno výstupního souboru. Například pro získání dat za okres Třebíč zadáme tyto argumenty:

1. argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6104

2. argument: vysledky_trebic.csv



Odkaz pro spuštění projektu:

py main.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6104' vysledky_trebic.csv



Ukázka projektu:

průběh stahování

STAHUJI DATA Z VYBRANE URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6104
VYSLEDKY ULOZENY DO: vysledky_trebic.csv
Ukončuji program.

částečný výstup

code;location;registered;envelopes;valid;ANO 2011;Blok proti islam.-Obran.domova;CESTA ODP...
590274;Babice;167;126;126;40;0;0;0;9;19;0;9;1;0;0;0;0;0;8;2;3;0;7;1;16;11;0;0
590282;Bačice;165;104;104;33;0;0;0;23;7;0;1;0;1;0;1;0;1;6;4;0;0;14;2;5;5;0;1
544833;Bačkovice;88;53;52;18;0;0;0;7;5;0;1;0;1;0;0;0;0;1;0;0;0;4;3;3;9;0;0
590304;Benetice;150;117;117;41;0;0;0;6;23;0;3;0;1;0;0;0;0;4;1;0;0;10;2;11;15;0;0