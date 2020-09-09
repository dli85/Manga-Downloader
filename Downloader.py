import sys
from bs4 import BeautifulSoup
import requests
import tkinter
import fpdf

cmdUsed = False
HELPMESSAGE = ''' Use the following extensions for more information:

--supported (gives a list of supported websites)
'''
SUPPORTEDSITES = ['https://mangakakalot.com/', 'https://manganelo.com/']

class Chapter:
    def __init__(self, title, link):
        self.title = title
        self.link = link

def crawlForChaptersType1(websiteLink, chapterListElementClassName):
    chapList = []
    chapterListData = requests.get(websiteLink)
    soupData = BeautifulSoup(chapterListData.text, 'html.parser')

    soupDataElems = soupData.findAll("div", {"class": "panel-story-chapter-list"})[0]
    listElem = soupDataElems.findAll('ul', {"class": "row-content-chapter"})[0]

    for i in listElem.find_all('li'):
        base = i.find_all('a')[0]
        title = base.getText()
        link = base['href']

        chapter = Chapter(title, link)

        chapList.append(chapter)

    return chapList


if __name__ == '__main__':


    args = sys.argv.copy()[1:]
    for i in range(len(args)):
        if '--' in args[i]:
            pass
        else:
            print("\nERROR: " + "\"" + args[i] + "\"" + ' not recognized as an extension \n')
            exit()

        if args[i] == '--help':
            print('\n' + HELPMESSAGE)
            exit()
        elif args[i] == '--supported':
            print('\n Downloading is available for the following websites: \n')
            for site in SUPPORTEDSITES:
                print(site + '\n')
            exit()

        if not cmdUsed:
            print("\nERROR: " + "\"" + args[i] + "\"" + ' not recognized as an extension \n')
            exit()


    websiteLink = input('\n What is the link of the Manga you would like to download (Website with of the chapter list of the manga): ')

    if 'manganelo' in websiteLink: #Type 1
        chapterList = crawlForChaptersType1(websiteLink, 'panel-story-chapter-list')

        #TODO get images and tkinter

    else:
        print('\nERROR: Website is either not supported or not recognized \n')

