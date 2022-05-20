import sys
import platform
import cv2
import time
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from fpdf import FPDF
import os
sys.path.insert(1, 'TTSToPdf')
from Page import SinglePage
from Frame import *
import tkinter as tk
#in tts cards files 
#cards in rows - 10
#cards in columns - 7


imageToConvertPath = ""
pathToSavePdf = ""
pathToSave = ""
pdfFileName = ""
pathOfTemplatesImages = ""
slashs = ""


if platform.system() == 'Windows':
	slashs = '\\'
else:
	slashs = '/'

def selectImage():
	file = filedialog.askopenfilename()
	textImageCard.delete(0,END)
	textImageCard.insert(0,file)
	global imageToConvertPath
	imageToConvertPath = os.path.abspath(file)
	global pathToSavePdf
	global pathOfTemplatesImages
	pathToSavePdf = os.path.dirname(imageToConvertPath)
	pathOfTemplatesImages = os.path.dirname(imageToConvertPath) + slashs + "TemplatesCards" + slashs
	if not os.path.isdir(pathOfTemplatesImages):
		os.mkdir(pathOfTemplatesImages)
	global pdfFileName
	newPdfFileName = os.path.splitext(imageToConvertPath)[0]
	pdfFileName = newPdfFileName.split(slashs)[len(newPdfFileName.split(slashs)) - 1] + ".pdf"
	#print(pathOfTemplatesImages)

def deleteAllTmps():
	dirName = os.path.split(imageToConvertPath)[0]
	test = os.listdir(dirName)
	for item in test:
		if item.endswith(".png"):
			os.remove(os.path.join(dirName,item))

def beginProcess():

	countOfCards = textCountCard.get()

	cardWidthForPdf = float(textWidthCard.get())
	cardHeigthForPdf = float(textHeightCard.get())

	row = 0
	col = 0

	pdf = FPDF()

	img = cv2.imread(imageToConvertPath)
	
	countOfCardsOnHorizontalInFile = int(textCountCardInFileHorizontal.get())
	countOfCardsOnVerticalInFile = int(textCountCardInFileOnVertical.get())

	rows = img.shape[0]
	cols = img.shape[1]

	frameWidth = cols/countOfCardsOnHorizontalInFile
	frameHeigth = rows/countOfCardsOnVerticalInFile

	mainFrame = Frame(int(frameWidth),int(frameHeigth))

	fileName = "FileNumber"

	imageIndex = 0

	if int(countCardOnHorizontalText.get()) == -12 and int(countCardOnVerticalText.get()) == -12: 
		pass

	else:
		
		cntOfCards = int(textCountCard.get())

		currentCardIndex = 1
		
		cardsPerPage = int(countCardOnHorizontalText.get()) * int(countCardOnVerticalText.get())
		currentCardsPerPage = cardsPerPage
		
		cardBack = img[0 + int(frameHeigth)*(countOfCardsOnVerticalInFile-1):0 + int(frameHeigth)*countOfCardsOnVerticalInFile,0 +int(frameWidth) * (countOfCardsOnHorizontalInFile-1):0 + int(frameWidth) * countOfCardsOnHorizontalInFile]
		cv2.imwrite(pathOfTemplatesImages + "cardBack.jpg",cardBack)

		while cntOfCards > 0:

			pdf.add_page()
			currentPage = SinglePage(  cardWidthForPdf,cardHeigthForPdf ,cardCountOnHorizontal = int(countCardOnHorizontalText.get()),cardCountOnVertical = int(countCardOnVerticalText.get()),spaceBetweenOnHorizontal = int(textCardsSpaceBetweenOnHorizontal.get()),spaceBetweenOnVertical = int(textCardsSpaceBetweenOnVertical.get()))
			for card in range(currentCardsPerPage):
				if cntOfCards > 0:
					crop = img[mainFrame.upBorder:mainFrame.downBorder, mainFrame.leftBorder:mainFrame.rightBorder]
					mainFrame.moveFrame("right")
					cv2.imwrite(pathOfTemplatesImages + fileName+str(imageIndex)+".png",crop)
					#print("new folder for tmp cards - " + pathOfTemplatesImages + fileName+str(imageIndex)+".png")
					newPos = currentPage.getLastFreePos()
					pdf.image(pathOfTemplatesImages+fileName+str(imageIndex)+".png",x=newPos[0],y=newPos[1],w=cardWidthForPdf,h=cardHeigthForPdf)
					currentCardIndex += 1
					imageIndex += 1																				
					if currentCardIndex == (countOfCardsOnHorizontalInFile + 1):
						mainFrame.moveFrame("down")
						mainFrame.moveFrame("beginColumn")
						currentCardIndex = 1
					cntOfCards-=1
				else:
					break
			if checkCardBackStyle.get() == 0:
				pdf.add_page()
				currentPage = SinglePage(  cardWidthForPdf,cardHeigthForPdf ,cardCountOnHorizontal = int(countCardOnHorizontalText.get()),cardCountOnVertical = int(countCardOnVerticalText.get()),spaceBetweenOnHorizontal = int(textCardsSpaceBetweenOnHorizontal.get()),spaceBetweenOnVertical = int(textCardsSpaceBetweenOnVertical.get()))
				for card in range(currentCardsPerPage):
					newPos = currentPage.getLastFreePos()
					pdf.image(pathOfTemplatesImages + "cardBack.jpg",x=newPos[0],y=newPos[1],w=cardWidthForPdf,h=cardHeigthForPdf)
		if checkCardBackStyle.get() == 1:
			pdf.add_page()
			currentPage = SinglePage(  cardWidthForPdf,cardHeigthForPdf ,cardCountOnHorizontal = int(countCardOnHorizontalText.get()),cardCountOnVertical = int(countCardOnVerticalText.get()),spaceBetweenOnHorizontal = int(textCardsSpaceBetweenOnHorizontal.get()),spaceBetweenOnVertical = int(textCardsSpaceBetweenOnVertical.get()))
			for card in range(currentCardsPerPage):
				newPos = currentPage.getLastFreePos()
				pdf.image(pathOfTemplatesImages + "cardBack.jpg",x=newPos[0],y=newPos[1],w=cardWidthForPdf,h=cardHeigthForPdf)
		pdf.output(str(pathToSavePdf )+slashs+pdfFileName) #windows shit
		if deleteTeplatesFiles.get() == 1:
			deleteAllTmps()
		messagebox.showinfo("Состояние процесса", "Преобразование готово")
		


#start gui section



window = Tk()
window.title("TTSToPdf")

deleteTeplatesFiles = IntVar()
checkCardBackStyle = IntVar()


countCardInFileHorizontalLabel = Label(window, text="Количество карт в файле по горизонтали")
countCardInFileHorizontalLabel.grid(column=0, row=0)

textCountCardInFileHorizontal = Entry(window,width=10)
textCountCardInFileHorizontal.grid(column=1, row=0)


countCardInFileVerticalLabel = Label(window, text="Количество карт в файле по вертикали")
countCardInFileVerticalLabel.grid(column=0, row=1)

textCountCardInFileOnVertical = Entry(window,width=10)
textCountCardInFileOnVertical.grid(column=1, row=1)


countCardLabel = Label(window, text="Количество карт")
countCardLabel.grid(column=0, row=2)

textCountCard = Entry(window,width=10)
textCountCard.grid(column=1, row=2)

emptyRow = Label(window, text="")
emptyRow.grid(column=0, row=3)

widthCardLable = Label(window, text="Ширина карт(мм)")
widthCardLable.grid(column=0, row=4)

textWidthCard = Entry(window,width=10)
textWidthCard.grid(column=1, row=4)

heightCardLabel = Label(window, text="Высота карт(мм)")
heightCardLabel.grid(column=0, row=5)

textHeightCard = Entry(window,width=10)
textHeightCard.grid(column=1, row=5)

emptyRow = Label(window, text="")
emptyRow.grid(column=0, row=6)

countCardOnHorizontalLabel = Label(window, text="Количество карт по горизонтали")
countCardOnHorizontalLabel.grid(column=0, row=7)

countCardOnHorizontalText = Entry(window,width=10)
countCardOnHorizontalText.grid(column=1, row=7)

countCardOnVerticalLabel = Label(window, text="Количество карт по вертикали")
countCardOnVerticalLabel.grid(column=0, row=8)

countCardOnVerticalText= Entry(window,width=10)
countCardOnVerticalText.grid(column=1, row=8)

emptyRow = Label(window, text="")
emptyRow.grid(column=0, row=9)

spaceBetweenCardsOnHorizontal = Label(window, text="Расстояние между картами по горизонтали(мм)")
spaceBetweenCardsOnHorizontal.grid(column=0, row=10)
textCardsSpaceBetweenOnHorizontal = Entry(window,width=10)
textCardsSpaceBetweenOnHorizontal.grid(column=1, row=10)


spaceBetweenCardsOnVertical = Label(window, text="Расстояние между картами по вертикали(мм)")
spaceBetweenCardsOnVertical.grid(column=0, row=11)
textCardsSpaceBetweenOnVertical = Entry(window,width=10)
textCardsSpaceBetweenOnVertical.grid(column=1, row=11)

emptyRow = Label(window, text="")
emptyRow.grid(column=0, row=12)

deleteTemplatesFilesLabel = Label(window, text="Удалить промежуточные файлы")
deleteTemplatesFilesLabel.grid(column=0, row=13)

deleteTemplatesCheckButton = Checkbutton(window,variable =deleteTeplatesFiles )
deleteTemplatesCheckButton.grid(column=1, row=13)

emptyRow = Label(window, text="")
emptyRow.grid(column=0, row=14)

cardBackStyleGenerationLAbel = Label(window, text="Вид генерации обложки")
cardBackStyleGenerationLAbel.grid(column=0, row=15)

radioButtonEveryPage = Radiobutton(window,text = "После каждой страницы",variable = checkCardBackStyle,value = 0) 
radioButtonEveryPage.grid(column = 1,row = 15)
radioButtonLastPage = Radiobutton(window,text = "На последней странице файла",variable = checkCardBackStyle,value = 1) 
radioButtonLastPage.grid(column = 1,row = 16)
radioButtonNoGenerate = Radiobutton(window,text = "Не генерировать",variable = checkCardBackStyle,value = 2) 
radioButtonNoGenerate.grid(column = 1,row = 17)

emptyRow = Label(window, text="")
emptyRow.grid(column=0, row=18)

selectImageButton = Button(window, text="Выбрать файл" ,command = selectImage)
selectImageButton.grid(column=0, row=19)
textImageCard = Entry(window,width=10)
textImageCard.grid(column=1, row=19)

startProcess = Button(window, text="Преобразовать" ,command = beginProcess)
startProcess.grid(column=0, row=20)

window.mainloop()


#end gui section