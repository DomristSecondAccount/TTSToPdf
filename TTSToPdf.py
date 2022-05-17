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
import tkinter as tk
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
		if deleteTeplatesFiles.get() == 1:
			deleteAllTmps()
		messagebox.showinfo("Состояние процесса", "Преобразование готово")
		


#start gui section



window = Tk()
window.title("TTSToPdf")

deleteTeplatesFiles = IntVar()
checkCardBackStyle = IntVar()

countCardLabel = Label(window, text="Количество карт")
countCardLabel.grid(column=0, row=0)

textCountCard = Entry(window,width=10)
textCountCard.grid(column=1, row=0)

emptyRow = Label(window, text="")
emptyRow.grid(column=0, row=1)

widthCardLable = Label(window, text="Ширина карт")
widthCardLable.grid(column=0, row=2)

textWidthCard = Entry(window,width=10)
textWidthCard.grid(column=1, row=2)

heightCardLabel = Label(window, text="Высота карт")
heightCardLabel.grid(column=0, row=3)

textHeightCard = Entry(window,width=10)
textHeightCard.grid(column=1, row=3)

emptyRow = Label(window, text="")
emptyRow.grid(column=0, row=4)

countCardOnHorizontalLabel = Label(window, text="Количество карт по горизонтали")
countCardOnHorizontalLabel.grid(column=0, row=5)

countCardOnHorizontalText = Entry(window,width=10)
countCardOnHorizontalText.grid(column=1, row=5)

countCardOnVerticalLabel = Label(window, text="Количество карт по вертикали")
countCardOnVerticalLabel.grid(column=0, row=6)

countCardOnVerticalText= Entry(window,width=10)
countCardOnVerticalText.grid(column=1, row=6)

emptyRow = Label(window, text="")
emptyRow.grid(column=0, row=7)

spaceBetweenCardsOnHorizontal = Label(window, text="Расстояние между картами по горизонтали")
spaceBetweenCardsOnHorizontal.grid(column=0, row=8)
textCardsSpaceBetweenOnHorizontal = Entry(window,width=10)
textCardsSpaceBetweenOnHorizontal.grid(column=1, row=8)


spaceBetweenCardsOnVertical = Label(window, text="Расстояние между картами по вертикали")
spaceBetweenCardsOnVertical.grid(column=0, row=9)
textCardsSpaceBetweenOnVertical = Entry(window,width=10)
textCardsSpaceBetweenOnVertical.grid(column=1, row=9)

emptyRow = Label(window, text="")
emptyRow.grid(column=0, row=10)

deleteTemplatesFilesLabel = Label(window, text="Удалить промежуточные файлы")
deleteTemplatesFilesLabel.grid(column=0, row=11)

deleteTemplatesCheckButton = Checkbutton(window,variable =deleteTeplatesFiles )
deleteTemplatesCheckButton.grid(column=1, row=11)

emptyRow = Label(window, text="")
emptyRow.grid(column=0, row=12)

cardBackStyleGenerationLAbel = Label(window, text="Вид генерации обложки")
cardBackStyleGenerationLAbel.grid(column=0, row=13)

radioButtonEveryPage = Radiobutton(window,text = "После каждой страницы",variable = checkCardBackStyle,value = 0) 
radioButtonEveryPage.grid(column = 1,row = 13)
radioButtonLastPage = Radiobutton(window,text = "На последней странице файла",variable = checkCardBackStyle,value = 1) 
radioButtonLastPage.grid(column = 1,row = 14)
radioButtonNoGenerate = Radiobutton(window,text = "Не генерировать",variable = checkCardBackStyle,value = 2) 
radioButtonNoGenerate.grid(column = 1,row = 15)

emptyRow = Label(window, text="")
emptyRow.grid(column=0, row=16)

selectImageButton = Button(window, text="Выбрать файл" ,command = selectImage)
selectImageButton.grid(column=0, row=17)
textImageCard = Entry(window,width=10)
textImageCard.grid(column=1, row=17)

startProcess = Button(window, text="Преобразовать" ,command = beginProcess)
startProcess.grid(column=0, row=18)

window.mainloop()


#end gui section