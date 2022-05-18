import sys
import cv2
import time
from tkinter import *
from tkinter import filedialog
from fpdf import FPDF
import os
sys.path.insert(1, 'TTSToPdf')
from Page import SinglePage

#in tts cards files 
#cards in rows - 10
#cards in columns - 7


imageToConvertPath = ""
pathToSave = ""

def selectImage():
	file = filedialog.askopenfilename()
	textImageCard.insert(0,file)
	global imageToConvertPath
	imageToConvertPath = os.path.abspath(file)
	print(imageToConvertPath)

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

	upBorder = 0
	downBorder = int(frameHeigth)

	leftBorder = 0
	rightBorder = int(frameWidth)

	heigthStep = int(frameHeigth)
	widthStep = int(frameWidth)

	#длинна 88,9 мм; ширина 57,15mm - стандартная игральная карта

	fileName = "FileNumber"

	leftBorder = col
	rightBorder = widthStep

	upBorder = row
	downBorder = heigthStep

	imageIndex = 0

	ceilAndRoundPart = getFullRows(countOfCards)

	for card in range(ceilAndRoundPart[0]):

		pdf.add_page()
		

		currentPage = SinglePage(  cardWidthForPdf,cardHeigthForPdf  )
		
		for cardIndex in range(9):
			
			crop = img[upBorder:downBorder, leftBorder:rightBorder] 
			cv2.imwrite(fileName+str(imageIndex)+".png",crop)
			newPos = currentPage.getLastFreePos()

			pdf.image(fileName+str(imageIndex)+".png",x=newPos[0],y =newPos[1],w = cardHeigthForPdf,h = cardHeigthForPdf)
			
			leftBorder += widthStep
			rightBorder += widthStep
			imageIndex+=1
		leftBorder = 0
		rightBorder = widthStep
		upBorder += heigthStep
		downBorder += heigthStep

	if int(ceilAndRoundPart[1]) > 0:

		pdf.add_page()
		currentPage = SinglePage(  cardWidthForPdf,cardHeigthForPdf  )

		for card in range(int(ceilAndRoundPart[1])):
			
			crop = img[upBorder:downBorder, leftBorder:rightBorder] 
			cv2.imwrite(fileName+str(imageIndex)+".png",crop)
			newPos = currentPage.getLastFreePos()

			pdf.image(fileName+str(imageIndex)+".png",x=newPos[0],y =newPos[1],w = cardWidthForPdf,h = cardHeigthForPdf)
			
			leftBorder += widthStep
			rightBorder += widthStep
			imageIndex+=1

	# почему именно 61 - потому-что у меня алгоритм так ебано работает, и если карт будет юольше 612 - то 
	#захвтится рубашка, листы которой долдны быть на отдельной странице

	if int(countOfCards) < 61: 
						 
		pdf.add_page()
		currentPage = SinglePage(cardWidthForPdf,cardHeigthForPdf)
		countOfTerationsOfColumns = int(countOfCards)%9
		leftBorder = widthStep * 9
		rightBorder = widthStep * 10
		upBorder = 0
		downBorder = heigthStep
		for card in range(countOfTerationsOfColumns):
			crop = img[upBorder:downBorder, leftBorder:rightBorder]
			cv2.imwrite(fileName+str(imageIndex)+".png",crop)
			newPos = currentPage.getLastFreePos()
			pdf.image(fileName+str(imageIndex)+".png",x=newPos[0],y=newPos[1],w=cardWidthForPdf,h=cardHeigthForPdf)
			upBorder += heigthStep
			downBorder += heigthStep
			imageIndex+=1		
			

	pdf.output("/home/di/FromCardPageToPdfCardsConverter/myPdf.pdf")
	deleteAllTmps()
	print("Done")


#start gui section

window = Tk()
window.title("TTSToPdf")

countCardLabel = Label(window, text="Количество карт")
countCardLabel.grid(column=0, row=0)

widthCardLable = Label(window, text="Ширина карт")
widthCardLable.grid(column=1, row=0)

heightCardLabel = Label(window, text="Высота карт")
heightCardLabel.grid(column=2, row=0)

textCountCard = Entry(window,width=10)
textCountCard.grid(column=0, row=1)

textWidthCard = Entry(window,width=10)
textWidthCard.grid(column=1, row=1)

textHeightCard = Entry(window,width=10)
textHeightCard.grid(column=2, row=1)


selectImageButton = Button(window, text="Выбрать файл" ,command = selectImage)
selectImageButton.grid(column=0, row=3)
textImageCard = Entry(window,width=10)
textImageCard.grid(column=1, row=3)

startProcess = Button(window, text="Преобразовать" ,command = beginProcess)
startProcess.grid(column=0, row=4)

window.mainloop()


#end gui section