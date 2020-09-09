import sys
from bs4 import BeautifulSoup
import requests
from tkinter import *
from tkinter import ttk
import fpdf

download = False

cmdUsed = False
HELPMESSAGE = ''' Use the following extensions for more information:

--supported (gives a list of supported websites)
'''
SUPPORTEDSITES = ['https://mangakakalot.com/', 'https://manganelo.com/']
#variables = []

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

def checkAll(variables):
    for i in variables:
        i.set(1)

def deSelectAll(variables):
    for i in variables:
        i.set(0)

def doGui(cList):
    toDownload = []

    variables = []

    master = Tk()

    topBarFrame = Frame(master)
    topBarFrame.pack()

    Label(topBarFrame, text='Please select which chapters to download: ').pack(padx=4, pady=4, side=LEFT, anchor=NW)
    Button(topBarFrame, text="Select all chapters", command= lambda: checkAll(variables)).pack(side=LEFT, anchor=NW)
    Button(topBarFrame, text="De-select all chapters", command= lambda: deSelectAll(variables)).pack(side=LEFT, anchor=NW)
    Button(topBarFrame, text="Download", command=master.quit, bg='#00FF00').pack(side=LEFT, anchor=NW)

    listFrame = Frame(master)
    canvas = Canvas(listFrame)
    scroll = Scrollbar(listFrame, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    #TODO bind mousewheel to scroll so it is possible to scroll with the mouse

    canvas.create_window((0, 0), window=scrollable_frame, anchor=NW)

    canvas.configure(yscrollcommand=scroll.set)


    for i in range(len(cList)):
        var = IntVar()
        variables.append(var)
        Checkbutton(scrollable_frame, text=cList[i].title, variable=var).pack(anchor=W)

    listFrame.pack(anchor=W, padx=4, fill=X)
    canvas.pack(side=LEFT, fill=Y, expand=True)
    scroll.pack(side=RIGHT, fill=Y)


    #listFrame.config(yscrollcommand=scroll.set)
    #scroll.config( command= listFrame.yview)

    mainloop()

    for i in range(len(variables)):
        if variables[i].get() == 1:
            toDownload.append(cList[i])

    return toDownload

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


    websiteLink = input('\nWhat is the link of the Manga you would like to download (Website with of the chapter list of the manga): ')

    if 'manganelo' in websiteLink: #Type 1
        chapterList = crawlForChaptersType1(websiteLink, 'panel-story-chapter-list')

        chaptersToDownload = doGui(chapterList)

        #TODO fetch images and make into pdf

    else:
        print('\nERROR: Website is either not supported or not recognized \n')

