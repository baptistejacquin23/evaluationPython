# Python 3
# Extraction des liens d'une page web
from __future__ import print_function, unicode_literals
from bs4 import BeautifulSoup
import urllib.request
import os
import sys
from time import sleep
import urllib
from PyInquirer import prompt, Separator
from examples import custom_style_2


class Lien:
    def __init__(self, index, nom, url):
        self.index = index
        self.nom = nom
        self.url = url


def getPageTitle(page):
    for title in page.find_all('h1', class_="firstHeading"):
        return title.getText()


def getPage(url):
    with urllib.request.urlopen(url) as response:
        webpage = response.read()
        soup = BeautifulSoup(webpage, 'html.parser')
    return soup


def formatageUrl(arg):
    urlStep1 = arg.replace(" ", "_")
    encodeUrl = urllib.parse.quote(urlStep1.encode('utf-8'))
    finalURL = encodeUrl.replace("%3A", ":")
    return finalURL


def findPageURLSearch(url):
    notEncodepageUrl = 'https://fr.wikipedia.org/wiki/{}'.format(getPageTitle(getPage(url)))
    encodePageUrl = formatageUrl(notEncodepageUrl)
    return encodePageUrl


def seedUrl(url):
    notEncodepageUrl = getPageTitle(getPage(url))
    encodePageUrl = notEncodepageUrl.replace(" ", "_")
    return encodePageUrl


def extractWebpage(soup, start, end, historique):
    # Nettoyage
    for annotNb in soup.find_all('sup', class_="reference"):
        annotNb.extract()
    for annotModif in soup.find_all('span', class_="mw-editsection"):
        annotModif.extract()
    for cadre in soup.find_all('div', class_="infobox"):
        cadre.extract()
    for cadre in soup.find_all('div', class_="infobox_v2"):
        cadre.extract()
    for cadre in soup.find_all('div', class_="infobox_v3"):
        cadre.extract()
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
    questions = [
        {
            'type': 'list',
            'name': 'theme',
            'message': 'Choisissez parmi les liens suivants : ',
            'choices': [
            ]
        },
    ]
    i = 1
    if tour > 1 and len(historique) > 1:
        questions[0].get("choices").append("0 => Retour à la page précédante")
        questions[0].get("choices").append(Separator(), )
    for anchor in soup.find('div', class_="mw-parser-output").find_all('a', href=True):
        if anchor.getText().strip() != '':
            if start <= i <= end:
                questions[0].get("choices").append(str(i) + ' => ' + str(anchor.getText()))
                i += 1
            else:
                i += 1
            listLiens.append(Lien(i, anchor.getText(), anchor['href']))

    questions[0].get("choices").append(Separator(), )
    if start >= 20:
        questions[0].get("choices").append("98 => Page précédante")
    if end <= len(listLiens):
        questions[0].get("choices").append("99 => Page Suivant")
    print("Total:", i - 1, "résultats")
    answers = prompt(questions, style=custom_style_2)

    return answers


def jeuTour(nb, finalUrl):
    currentUrl = history[-1]
    currentPage = getPage(currentUrl)
    global paginationLimite
    global paginationstart
    global tour
    print("🌊🌊🌊🌊🌊 Wikigame 🌊🌊🌊🌊🌊", "Tour :", nb)
    print("🏁 Départ :", getPageTitle(pageBase) + " 🏁")
    print("🎯 Cible :", getPageTitle(pageArrivée) + " 🎯")
    print("🚩 Actuel :", getPageTitle(currentPage) + " 🚩")
    result = extractWebpage(currentPage, paginationstart, paginationLimite, history)
    choix = result["theme"].split(' ', 1)[0]
    choixFullString = result["theme"]
    try:
        if choix == "0" and nb > 0:
            history.pop()
            historyToDisplay.append(getPageTitle(getPage(history[-1])))
            paginationLimite = 20
            paginationstart = 1
        if "99 => Page Suivant" in choixFullString:
            paginationLimite += 20
            paginationstart += 20
            tour -= 1
        if "98 => Page précédante" in choixFullString:
            paginationLimite -= 20
            paginationstart -= 20
            tour -= 1
        if paginationstart <= int(
                choix) <= paginationLimite and "99 => Page Suivant" not in choixFullString and "98 => Page précédante" not in choixFullString:
            choixSelectedIndex = int(choix) - 1
            history.append("https://fr.wikipedia.org" + str(listLiens[choixSelectedIndex].url))
            historyToDisplay.append(
                getPageTitle(getPage("https://fr.wikipedia.org" + str(listLiens[choixSelectedIndex].url))))
            currentUrl = history[-1]
            paginationLimite = 20
            paginationstart = 1
        if finalUrl == currentUrl:
            global fin
            fin = True
    except ValueError:
        tour -= 1
        print("Erreur de Saisie!! Un nombre afficher sur l'ecran est attendu");
        sleep(3)


# Main
tour = 1
fin = False
paginationLimite = 20
paginationstart = 1
listLiens = []
history = []
historyToDisplay = []
urlRandom = 'https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard'
if len(sys.argv) == 1:
    firstPageUrl = findPageURLSearch(urlRandom)
    toGoUrl = findPageURLSearch(urlRandom)
    pageBase = getPage(firstPageUrl)
    pageArrivée = getPage(toGoUrl)
    history.append(firstPageUrl)
elif len(sys.argv) == 3:
    paramUrl = sys.argv[2]
    arrayOfParam = paramUrl.split("#")
    firstPageUrl = findPageURLSearch("https://fr.wikipedia.org/wiki/" + formatageUrl(arrayOfParam[0]))
    toGoUrl = findPageURLSearch("https://fr.wikipedia.org/wiki/" + formatageUrl(arrayOfParam[1]))
    pageBase = getPage(firstPageUrl)
    pageArrivée = getPage(toGoUrl)
    history.append(firstPageUrl)

if len(sys.argv) == 1 or len(sys.argv) == 3 and sys.argv[1] == "-s":
    while not fin == True:
        os.system('cls||clear')
        jeuTour(tour, toGoUrl)
        listLiens.clear()
        tour += 1

    os.system('cls||clear')
    print("🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊")
    print("🎊 Vous avez gagné !!!!!!!! En " + str(tour - 1) + " tours 🎊")
    print("🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊")
    print("Voici les pages que vous avez visité :")
    print("Page de départ : " + getPageTitle(getPage(history[0])))
    for idx, val in enumerate(historyToDisplay):
        if idx + 1 == len(historyToDisplay):
            print("Page d'arrivée : " + historyToDisplay[-1])
        else:
            print("Page n°" + str(idx + 1) + "         " + str(val))
    print("🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊")
elif len(sys.argv) == 2 and sys.argv[1] == "-n":
    os.system('cls||clear')
    print("✅  ✅  ✅ Génération réussi ✅  ✅  ✅  ")
    print("lancer la commande ci-dessous : ")
    print('python3 realGame.py -s "' + seedUrl(urlRandom) + '#' + seedUrl(urlRandom) + '"')
else:
    os.system('cls||clear')
    print("❌️ ERROR️ ❌️")
    print("🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴")
    print("Pour lancer le jeu 3 options s'offre à vous :️")
    print("🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴")
    print("1) lancer le jeu avec des url au hasard avec la commande :️")
    print("python3 realGame.py")
    print("🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴")
    print("2) Generer une graine avec la commande :️")
    print("python3 realGame.py -n")
    print("🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴")
    print("3) Lance une partie avec une graine avec la commande :️")
    print("python3 realGame.py -s premiereURL#deuxiemeURL")
    print("Exemple : ")
    print("python3 realGame.py -s Andasta_benoiti#Henri_Durville")
    print("🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴")
