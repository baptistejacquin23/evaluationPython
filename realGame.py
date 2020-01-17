# Python 3
# Extraction des liens d'une page web
from bs4 import BeautifulSoup
import urllib.request
import os
import sys
import copy
from time import sleep


class Lien():
    def __init__(self, index, nom, url):
        self.index = index
        self.nom = nom
        self.url = url


def getPageTitle(page):
    # Get title
    for title in page.find_all('h1', class_="firstHeading"):
        return title.getText()


def getPage(url):
    with urllib.request.urlopen(url) as response:
        webpage = response.read()
        soup = BeautifulSoup(webpage, 'html.parser')
    return soup


def findPageSearch(url):
    with urllib.request.urlopen(url) as response:
        webpage = response.read()
        soup = BeautifulSoup(webpage, 'html.parser')
        title = soup.select('h1.firstHeading')[0].text.strip()
        titreUrl = str(title).split(' ', 1)[0]
        hrefs = soup.find_all('link')
        for url in hrefs:
            if str(url['href']).__contains__("https://fr.wikipedia.org/wiki/" + titreUrl):
                return url['href']


def extractWebpage(soup, start, end):
    # Nettoyage
    for annotNb in soup.find_all('sup', class_="reference"):
        annotNb.extract()
    for annotModif in soup.find_all('span', class_="mw-editsection"):
        annotModif.extract()
    for cadre in soup.find_all('table', class_="infobox"):
        cadre.extract()
    for cadre in soup.find_all('table', class_="infobox_v2"):
        cadre.extract()
    for cadre in soup.find_all('table', class_="infobox_v3"):
        cadre.extract()
    for portail in soup.find_all('ul', class_="bandeau-portail"):
        portail.extract()
    for navbox in soup.find_all('div', class_="navbox-container"):
        navbox.extract()
    for image in soup.find_all('div', class_="image"):
        image.extract()
    for en in soup.find_all('a', class_="extiw"):
        en.extract()
    for agrandir in soup.find_all('a', class_="internal"):
        agrandir.extract()
    for phono in soup.find_all('a', class_="mw-redirect"):
        phono.extract()
    for sommaire in soup.find_all('div', class_="toc"):
        sommaire.extract()
    for refcadre in soup.find_all('div', class_="reference-cadre"):
        refcadre.extract()
    for homonime in soup.find_all('div', class_="homonymie"):
        homonime.extract()
    for ebauche in soup.find_all('div', class_="bandeau-article"):
        ebauche.extract()


    # Affiche lien retour + liens et compte
    i = 1
    if tour > 1:
        print("0 => retour")
    for anchor in soup.find('div', class_="mw-parser-output").find_all('a', href=True):
        if anchor.getText().strip() != '':
            if start <= i <= end:
                print(i, '=>', anchor.getText())
                i += 1
            else:
                i += 1
            listLiens.append(Lien(i, anchor.getText(), anchor['href']))
    print("98 => Page précédante")
    print("99 => Page Suivant")
    print("Total:", i - 1, "résultats")


def jeuTour(nb, toGoUrl):
    currentUrl = history[-1]
    currentPage = getPage(currentUrl)
    global paginationLimite
    global paginationstart
    global tour
    # if while fin == False:
    print("********** Wikigame **********", "-", "Tour :", nb)
    print("Départ :", getPageTitle(pageBase))
    print("Cible :", getPageTitle(pageArrivée))
    print("Actuel :", getPageTitle(currentPage))
    extractWebpage(currentPage, paginationstart, paginationLimite)
    choix = input("votre choix :")
    try:
        if choix == "0" and nb > 0:
            history.pop()
        if choix == "99":
            paginationLimite += 20
            paginationstart += 20
            tour -= 1
        if choix == "98":
            paginationLimite -= 20
            paginationstart -= 20
            tour -= 1
        if paginationstart <= int(choix) <= paginationLimite:
            choixSelectedIndex = int(choix) - 1
            history.append("https://fr.wikipedia.org" + str(listLiens[choixSelectedIndex].url))
            currentUrl = history[-1]
        if toGoUrl == currentUrl:
            global fin
            fin = True
    except ValueError:
        tour -= 1
        print("Erreur de Saisie!! Un nombre afficher sur l'ecran est attendu"); sleep(3)



# Main
tour = 1
fin = False
paginationLimite = 20
paginationstart = 1
urlRandom = 'https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard'
firstPageUrl = findPageSearch(urlRandom)
toGoUrl = findPageSearch(urlRandom)
listLiens = []
history = []

pageBase = getPage(firstPageUrl)
pageArrivée = getPage(toGoUrl)

history.append(firstPageUrl)

while fin == False:
    os.system('cls||clear')
    jeuTour(tour, toGoUrl)
    listLiens.clear()
    tour += 1

print("Vous avez gagné !!!!!!!! En " + str(tour - 1) + " tours")
