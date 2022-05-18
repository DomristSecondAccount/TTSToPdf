#сделать проверку на нули в значениях

import cv2
import time
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from fpdf import FPDF
import os
from Page import SinglePage
from Frame import *

#in tts cards files 
#cards in rows - 10
#cards in columns - 7


imageToConvertPath = ""
pathToSavePdf = ""
pathToSave = ""
pdfFileName = ""
pathOfTemplatesImages = ""

def selectImage():
	file = filedialog.askopenfilename()
	textImageCard.delete(0,END)
	textImageCard.insert(0,file)
	global imageToConvertPath
	imageToConvertPath = os.path.abspath(file)
	global pathToSavePdf
	global pathOfTemplatesImages
	pathToSavePdf = os.path.dirname(imageToConvertPath)
	pathOfTemplatesImages = os.path.dirname(imageToConvertPath) + "/"
	global pdfFileName
	newPdfFileName = os.path.splitext(imageToConvertPath)[0]
	pdfFileName = newPdfFileName.split("/")[len(newPdfFileName.split("/")) - 1] + ".pdf"
	print(pathOfTemplatesImages)

def deleteAllTmps():
	dirName = os.path.split(imageToConvertPath)[0]
	test = os.listdir(dirName)
	for item in test:
		if item.endswith(".png"):
			os.remove(os.path.join(dirName,item))

def getFullRows(countOfCards): #ну я тут хер знает как обозвать целую и дробную чась
	ceilPart = int(int(countOfCards)/10)
	roundPart = int(countOfCards) // 10**0 % 10
	return [ceilPart,roundPart]

def beginProcess():

	countOfCards = textCountCard.get()

	cardWidthForPdf = float(textWidthCard.get())
	cardHeigthForPdf = float(textHeightCard.get())

	row = 0
	col = 0

	pdf = FPDF()

	img = cv2.imread(imageToConvertPath)
	
	rows = img.shape[0]
	cols = img.shape[1]

	frameWidth = cols/10
	frameHeigth = rows/7

	mainFrame = Frame(int(frameWidth),int(frameHeigth))

	#длинна 88,9 мм; ширина 57,15mm - стандартная игральная карта

	fileName = "FileNumber"

	imageIndex = 0

	#вот этот if надо будет потом к херам вырезать, совершенно дегенератский алгоритм
	if int(countCardOnHorizontalText.get()) == -12 and int(countCardOnVerticalText.get()) == -12: 
		pass

	else:
		
		cntOfCards = int(textCountCard.get())
		
		currentCardIndex = 1 #вот здесь лучше индексировать от единицы так как я тупой
		
		cardsPerPage = int(countCardOnHorizontalText.get()) * int(countCardOnVerticalText.get())
		currentCardsPerPage = cardsPerPage
		
		while cntOfCards > 0:

			pdf.add_page()
			currentPage = SinglePage(  cardWidthForPdf,cardHeigthForPdf ,cardCountOnHorizontal = int(countCardOnHorizontalText.get()),cardCountOnVertical = int(countCardOnVerticalText.get()),spaceBetweenOnHorizontal = int(textCardsSpaceBetweenOnHorizontal.get()),spaceBetweenOnVertical = int(textCardsSpaceBetweenOnVertical.get()))
			for card in range(currentCardsPerPage): #добавляем n карт на последнюю pdf страницу
				if cntOfCards > 0:
					crop = img[mainFrame.upBorder:mainFrame.downBorder, mainFrame.leftBorder:mainFrame.rightBorder]
					mainFrame.moveFrame("right")
					cv2.imwrite(pathOfTemplatesImages + fileName+str(imageIndex)+".png",crop)
					newPos = currentPage.getLastFreePos()
					pdf.image(pathOfTemplatesImages+fileName+str(imageIndex)+".png",x=newPos[0],y=newPos[1],w=cardWidthForPdf,h=cardHeigthForPdf)
					currentCardIndex += 1
					imageIndex += 1																				
					if currentCardIndex == 11: #если упёрлись в последнюю карту - прыгаем на первую колонку следующего ряда
						mainFrame.moveFrame("down")
						mainFrame.moveFrame("beginColumn")
						currentCardIndex = 1
					cntOfCards-=1
				else:
					break
		pdf.output(str(pathToSavePdf )+"/"+pdfFileName)
		deleteAllTmps()
		messagebox.showinfo("Process state", "Done")
		


#start gui section

window = Tk()
window.title("TTSToPdf")

countCardLabel = Label(window, text="Number of cards")
countCardLabel.grid(column=0, row=0)

textCountCard = Entry(window,width=10)
textCountCard.grid(column=1, row=0)

widthCardLable = Label(window, text="Card Width")
widthCardLable.grid(column=0, row=1)

textWidthCard = Entry(window,width=10)
textWidthCard.grid(column=1, row=1)

heightCardLabel = Label(window, text="Card Height")
heightCardLabel.grid(column=0, row=2)

textHeightCard = Entry(window,width=10)
textHeightCard.grid(column=1, row=2)

countCardOnHorizontalLabel = Label(window, text="Number of cards horizontally")
countCardOnHorizontalLabel.grid(column=0, row=3)

countCardOnHorizontalText = Entry(window,width=10)
countCardOnHorizontalText.grid(column=1, row=3)

countCardOnVerticalLabel = Label(window, text="Number of cards vertically")
countCardOnVerticalLabel.grid(column=0, row=4)

countCardOnVerticalText= Entry(window,width=10)
countCardOnVerticalText.grid(column=1, row=4)

spaceBetweenCardsOnHorizontal = Label(window, text="Horizontal distance between cards")
spaceBetweenCardsOnHorizontal.grid(column=0, row=5)
textCardsSpaceBetweenOnHorizontal = Entry(window,width=10)
textCardsSpaceBetweenOnHorizontal.grid(column=1, row=5)


spaceBetweenCardsOnVertical = Label(window, text="Vertical distance between cards")
spaceBetweenCardsOnVertical.grid(column=0, row=6)
textCardsSpaceBetweenOnVertical = Entry(window,width=10)
textCardsSpaceBetweenOnVertical.grid(column=1, row=6)

selectImageButton = Button(window, text="Select a file" ,command = selectImage)
selectImageButton.grid(column=0, row=7)
textImageCard = Entry(window,width=10)
textImageCard.grid(column=1, row=7)

startProcess = Button(window, text="Convert" ,command = beginProcess)
startProcess.grid(column=0, row=8)

window.mainloop()


#end gui section