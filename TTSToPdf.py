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

	mainFrame = Frame(int(frameWidth),int(frameHeigth))
	print("Frame width = " + str(mainFrame.frameWidth))
	print("Frame height = " + str(mainFrame.frameHeight))
	#длинна 88,9 мм; ширина 57,15mm - стандартная игральная карта

	fileName = "FileNumber"

	imageIndex = 0

	#вот этот if надо будет потом к херам вырезать, совершенно дегенератский алгоритм
	if int(countCardOnHorizontalText.get()) == -12 and int(countCardOnVerticalText.get()) == -12: 
		ceilAndRoundPart = getFullRows(countOfCards)

		for card in range(ceilAndRoundPart[0]):

			pdf.add_page()

			currentPage = SinglePage(  cardWidthForPdf,cardHeigthForPdf  )
			
			for cardIndex in range(9):
				
				crop = img[mainFrame.upBorder:mainFrame.downBorder, mainFrame.leftBorder:mainFrame.rightBorder] 
				cv2.imwrite(fileName+str(imageIndex)+".png",crop)
				newPos = currentPage.getLastFreePos()

				pdf.image(fileName+str(imageIndex)+".png",x=newPos[0],y =newPos[1],w = cardHeigthForPdf,h = cardHeigthForPdf)
				mainFrame.moveFrame("right")
				imageIndex+=1

			mainFrame.moveFrame("beginColumn")
			mainFrame.moveFrame("down")
			

		if int(ceilAndRoundPart[1]) > 0:

			pdf.add_page()
			currentPage = SinglePage(  cardWidthForPdf,cardHeigthForPdf  )

			for card in range(int(ceilAndRoundPart[1])):
				
				crop = img[mainFrame.upBorder:mainFrame.downBorder, mainFrame.leftBorder:mainFrame.rightBorder] 
				cv2.imwrite(fileName+str(imageIndex)+".png",crop)
				newPos = currentPage.getLastFreePos()

				pdf.image(fileName+str(imageIndex)+".png",x=newPos[0],y =newPos[1],w = cardWidthForPdf,h = cardHeigthForPdf)
				mainFrame.moveFrame("right")
				#leftBorder += widthStep
				#rightBorder += widthStep
				imageIndex+=1

		# почему именно 61 - потому-что у меня алгоритм так ебано работает, и если карт будет юольше 612 - то 
		#захвтится рубашка, листы которой долдны быть на отдельной странице

		if int(countOfCards) < 61: 
							 
			pdf.add_page()
			currentPage = SinglePage(cardWidthForPdf,cardHeigthForPdf)
			countOfTerationsOfColumns = int(countOfCards)%9
			
			mainFrame.moveFrame("endColumn")
			mainFrame.upBorder = 0
			mainFrame.downBorder = mainFrame.frameHeight

			for card in range(countOfTerationsOfColumns):
				crop = img[mainFrame.upBorder:mainFrame.downBorder, mainFrame.leftBorder:mainFrame.rightBorder]
				cv2.imwrite(fileName+str(imageIndex)+".png",crop)
				newPos = currentPage.getLastFreePos()
				pdf.image(fileName+str(imageIndex)+".png",x=newPos[0],y=newPos[1],w=cardWidthForPdf,h=cardHeigthForPdf)
				mainFrame.moveFrame("down")
				
				imageIndex+=1		
				

		pdf.output("/home/di/FromCardPageToPdfCardsConverter/myPdf.pdf")
		deleteAllTmps()
		print("Done")

	else:
		print("Start custom")
		
		cntOfCards = int(textCountCard.get())
		
		currentCardIndex = 1 #вот здесь лучше индексировать от единицы так как я тупой
		
		cardsPerPage = int(countCardOnHorizontalText.get()) * int(countCardOnVerticalText.get())
		currentCardsPerPage = cardsPerPage
		
		while cntOfCards > 0:

			pdf.add_page()
			currentPage = SinglePage(  cardWidthForPdf,cardHeigthForPdf ,cardCountOnHorizontal = int(countCardOnHorizontalText.get()),cardCountOnVertical = int(countCardOnVerticalText.get()))
			for card in range(currentCardsPerPage): #добавляем n карт на последнюю pdf страницу
				if cntOfCards > 0:
					crop = img[mainFrame.upBorder:mainFrame.downBorder, mainFrame.leftBorder:mainFrame.rightBorder]
					mainFrame.moveFrame("right")
					cv2.imwrite(fileName+str(imageIndex)+".png",crop)
					newPos = currentPage.getLastFreePos()
					pdf.image(fileName+str(imageIndex)+".png",x=newPos[0],y=newPos[1],w=cardWidthForPdf,h=cardHeigthForPdf)
					currentCardIndex += 1
					imageIndex += 1																				
					if currentCardIndex == 11: #если упёрлись в последнюю карту - прыгаем на первую колонку следующего ряда
						mainFrame.moveFrame("down")
						mainFrame.moveFrame("beginColumn")
						currentCardIndex = 1
					cntOfCards-=1
				else:
					break
		pdf.output("/home/di/FromCardPageToPdfCardsConverter/myPdf.pdf")
		deleteAllTmps()
		messagebox.showinfo("Состояние процесса", "Преобразование готово")
		


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

countCardOnHorizontalLabel = Label(window, text="Количество карт по горизонтале")
countCardOnHorizontalLabel.grid(column=0, row=3)

countCardOnHorizontalText = Entry(window,width=10)
countCardOnHorizontalText.grid(column=1, row=3)

countCardOnVerticalLabel = Label(window, text="Количество карт по вертикале")
countCardOnVerticalLabel.grid(column=0, row=4)

countCardOnVerticalText= Entry(window,width=10)
countCardOnVerticalText.grid(column=1, row=4)


selectImageButton = Button(window, text="Выбрать файл" ,command = selectImage)
selectImageButton.grid(column=0, row=5)
textImageCard = Entry(window,width=10)
textImageCard.grid(column=1, row=5)

startProcess = Button(window, text="Преобразовать" ,command = beginProcess)
startProcess.grid(column=0, row=6)

window.mainloop()


#end gui section