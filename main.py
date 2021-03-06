import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from IT_2021 import *
import os

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('test.ui')
form_class = uic.loadUiType(form)[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.path=('','')
        self.imagePath=('','')
        self.spinBox.setMaximum(999)


        self.pushButton.clicked.connect(self.loadImageFromFile)
        self.excelBtn.clicked.connect(self.loadExcelFromFile)
        self.showBtn.clicked.connect(self.showReceiptData)
        self.showListBtn.clicked.connect(self.showList)

    def loadImageFromFile(self):
        if self.path[0]=='':
            QMessageBox.about(self,'CSV 파일 없음','CSV 파일을 먼저 불러와주세요!')
            return print('없음')
        self.imagePath=QFileDialog.getOpenFileName(self,"Open Image", './', "Image Files (*.png *.jpg *.bmp *.jpeg)")
        if self.imagePath==('',''):
            return
        if self.imagePath:
            print(self.imagePath)
            self.qPixmapFileVar=QPixmap()
            self.qPixmapFileVar.load(self.imagePath[0])
            self.qPixmapFileVar=self.qPixmapFileVar.scaledToWidth(400)
            self.qPixmapFileVar = self.qPixmapFileVar.scaledToHeight(600)
            self.label.setPixmap(self.qPixmapFileVar)
        result=main(self.imagePath[0])
        self.ocr_date=result[0]
        self.ocr_price=result[1]
        print(self.ocr_date,self.ocr_price)
        p_ocr_date=self.ocr_date[:4]+'.'+self.ocr_date[4:6]+'.'+self.ocr_date[6:]
        self.tableWidget_2.setRowCount(1)
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setHorizontalHeaderLabels(["날짜", "금액"])
        self.tableWidget_2.setItem(0, 0, QTableWidgetItem(p_ocr_date))
        self.tableWidget_2.setItem(0, 1, QTableWidgetItem(self.ocr_price))
        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_2.resizeRowsToContents()
        # print(ocr_date, type(ocr_price))

    def loadExcelFromFile(self):
        self.path=QFileDialog.getOpenFileName(self,"Open Csv", './', "Csv Files (*.csv)")
        if self.path==('',''):
            return
        self.all_data=pd.read_csv(self.path[0],encoding='euc-kr')
        self.all_data=self.all_data[['날짜', '영수증번호', ' 상세내용 ', ' 지출 ']]
        self.tableWidget.setColumnCount(len(self.all_data.columns))
        self.tableWidget.setRowCount(len(self.all_data))
        self.tableWidget.setHorizontalHeaderLabels(self.all_data.columns)
        for i in range(len(self.all_data)):
            for j in range(len(self.all_data.columns)):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.all_data.iat[i, j])))
        self.tableWidget.resizeColumnsToContents()

    def showReceiptData(self):
        if self.path[0]=='':
            QMessageBox.about(self,'CSV 파일 없음','CSV 파일을 먼저 불러와주세요!')
            return print('없음')
        if self.imagePath[0]=='':
            QMessageBox.about(self,'영수증 파일 없음','영수증 이미지를 불러와주세요!')
            return print('없음')

        receiptNum=self.spinBox.value()
        print(receiptNum)

        self.selected_data = self.all_data[self.all_data['영수증번호']==receiptNum]
        self.tableWidget.setColumnCount(len(self.selected_data.columns))
        self.tableWidget.setRowCount(len(self.selected_data))
        self.tableWidget.setHorizontalHeaderLabels(self.selected_data.columns)
        for i in range(len(self.selected_data)):
            for j in range(len(self.selected_data.columns)):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.selected_data.iat[i, j])))
        self.tableWidget.resizeColumnsToContents()

        if len(self.selected_data)!=0:
            self.excel_date=self.selected_data.iat[0,0]
            self.excel_date = self.excel_date.replace(".","")
            self.excel_price=self.selected_data.iat[0,3]
            print(self.excel_date, self.excel_price)
            # print(self.ocr_date, self.ocr_price)
            print(self.excel_date==self.ocr_date)
            print((int)(self.excel_price)==(int)(self.ocr_price))

            if self.excel_date==self.ocr_date and (int)(self.excel_price)==(int)(self.ocr_price):
                QMessageBox.about(self, '데이터 비교하기', '날짜와 금액이 모두 일치합니다!')
            elif self.excel_date == self.ocr_date and (int)(self.excel_price) != (int)(self.ocr_price):
                QMessageBox.about(self, '데이터 비교하기', '금액이 일치하지 않습니다!')
            elif self.excel_date != self.ocr_date and (int)(self.excel_price) == (int)(self.ocr_price):
                QMessageBox.about(self, '데이터 비교하기', '날짜가 일치하지 않습니다!')
            elif self.excel_date != self.ocr_date and (int)(self.excel_price) != (int)(self.ocr_price):
                QMessageBox.about(self, '데이터 비교하기', '날짜와 금액이 모두 일치하지 않습니다!')


    def showList(self):
        if self.path[0]=='':
            QMessageBox.about(self, 'CSV 파일 없음', 'CSV 파일을 먼저 불러와주세요!')
            return print('없음')
        self.all_data = self.all_data[['날짜', '영수증번호', ' 상세내용 ', ' 지출 ']]
        self.tableWidget.setColumnCount(len(self.all_data.columns))
        self.tableWidget.setRowCount(len(self.all_data))
        self.tableWidget.setHorizontalHeaderLabels(self.all_data.columns)
        for i in range(len(self.all_data)):
            for j in range(len(self.all_data.columns)):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.all_data.iat[i, j])))
        self.tableWidget.resizeColumnsToContents()
        self.spinBox.setValue(0)

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    myWindow.setFixedSize(myWindow.size())
    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
