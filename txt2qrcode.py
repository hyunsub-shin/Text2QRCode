from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import *
# for Add logo
from PIL import Image
from PyQt5.QtWidgets import QFileDialog

import os
import sys

## pip install qrcode ##
import qrcode


####################################################
app = QtWidgets.QApplication([])
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ui_file = os.path.join(BASE_DIR, 'txt2qrcode.ui')

# 운영체제 확인 및 경로 설정
if os.name == 'nt':  # Windows
    ui_file = ui_file.replace('/', '\\')
else:  # Linux/Unix
    ui_file = ui_file.replace('\\', '/')

ui = uic.loadUi(ui_file)
ui.setWindowTitle("Text to QR Code - made by hsshin")
####################################################


###############
## Variables ##
###############
# init background color 'block'
back_r = 255
back_b = 255
back_g = 255
back_col = QColor(back_r, back_g, back_b)
back_frm = ui.label_back_color
back_frm.setStyleSheet('QWidget {background-color: %s }' % back_col.name())

# init background color 'white'
text_r = 0
text_g = 0
text_b = 0
text_col = QColor(text_r, text_g, text_b)
text_frm = ui.label_text_color
text_frm.setStyleSheet('QWidget {background-color: %s }' % text_col.name())

logo_enable = 0

## USE qrcode ##
def Gen_QRCode():
    ver = ui.lineEdit_qr_ver.text()
    dot_size = ui.lineEdit_dot_size.text()
    border_size = ui.lineEdit_border_size.text()
    img_size = ui.lineEdit_img_size.text()
    
    qr = qrcode.QRCode(version=int(ver), 
                       box_size=int(dot_size), 
                       border=int(border_size), 
                       error_correction=qrcode.constants.ERROR_CORRECT_H)
    
    data = ui.textEdit_input.toPlainText()
    qr.add_data(data)

    # Make the QR code
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color=text_col.name(), back_color=back_col.name())
    
    if(logo_enable == True):
        #### Add Logo ####
        # 로고 이미지 열기
        logo = Image.open(sel_logo)
        # 로고 이미지 크기 조정
        logo_size = int(min(img.size) / 4)
        logo = logo.resize([logo_size, logo_size])
        # QR 코드 이미지에 로고 붙이기
        img.paste(logo, box=(int((img.size[0] - logo_size) / 2), int((img.size[1] - logo_size) / 2)))
        ####################
    
    # image resize
    img = img.resize([int(img_size),int(img_size)])
    
    # Save the QR code image
    img.save("qrcode_gen.png")

    # diplay image
    qPixmapVar = QPixmap()
    qPixmapVar.load("qrcode_gen.png")
    
    # ui.label_qrcode.setPixmap(qPixmapVar)
    # fixed scale 150x150
    ui.label_qrcode.setPixmap(qPixmapVar.scaled(200, 200))
    
    
def SetBackgroundColor():
    global back_col, back_r, back_g, back_b
    back_col = QtWidgets.QColorDialog.getColor()
    
    if back_col.isValid():
        back_frm.setStyleSheet('QWidget { background-color: %s }' % back_col.name())
        
        rgb = back_col.getRgb()
        # print(rgb)      
        back_r = rgb[0]
        back_g = rgb[1]
        back_b = rgb[2]
        # print(back_r)
        # print(back_g)
        # print(back_b)


def SetTextColor():
    global text_col, text_r, text_g, text_b
    text_col = QtWidgets.QColorDialog.getColor()
    
    if text_col.isValid():
        text_frm.setStyleSheet('QWidget { background-color: %s }' % text_col.name())
        
        rgb = text_col.getRgb()
        # print(rgb)      
        text_r = rgb[0]
        text_g = rgb[1]
        text_b = rgb[2]
        # print(text_r)
        # print(text_g)
        # print(text_b)
        

def input_logo(state):
    global logo_enable, sel_logo
    
    if state == 2:
        logo_enable = 1
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog 
        logo_file, _ = QFileDialog.getOpenFileName(None, "logo", "그림 파일 (*.png *.bmp *.jpg);;모든 파일 (*)", options=options)
        if logo_file:
            print(f"선택한 그림: {logo_file}")
            sel_logo = logo_file
        else:
            ui.checkBox_logo_enable.setCheckState(False)
            logo_enable = 0
    else:
        # ui.checkBox_logo_enable.setCheckState(False)
        logo_enable = 0        
    
        
ui.pushButton_gen_qr.clicked.connect(Gen_QRCode)
ui.pushButton_back_color.clicked.connect(SetBackgroundColor)
ui.pushButton_text_color.clicked.connect(SetTextColor)
ui.checkBox_logo_enable.stateChanged.connect(input_logo)


ui.show()

# CI 환경에서 실행 중인지 확인
if os.environ.get('CI'):
    # 3초 후 앱 종료
    QtCore.QTimer.singleShot(3000, app.quit)

sys.exit(app.exec_())





