from tkinter import *
from tkinter.filedialog import askopenfilename
import cv2
import pytesseract
from tkinter.ttk import Checkbutton

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def run():
    filename = askopenfilename()
    print(filename)
    image = cv2.imread(filename)
    if var4.get() == 0:
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        img = 255 - opening
        cv2.waitKey()

    config = r'--oem 3 --psm 6'
    config1 = '--psm 10'
    config2 = 'no digits -psm 7'
    language = 'rus+eng'
    if var1.get() == 1 and var2.get() == 1:
        language = 'rus+eng'
    elif var1.get() == 1:
        language = 'rus'
    elif var2.get() == 1:
        language = 'eng'

    data = pytesseract.image_to_string(img, lang=language, config=config)
    for i in data:
        if i not in "йцукенгшщзхъфывапролджэячсмитьбю." \
                    "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ," \
                    "qwertyuiop[]asdfghjkl;'zxcvbnm,./" \
                    "QWERTYUIOP{}ASDFGHJKL:ZXCVBNM<>?" \
                    " 1234567890-=!@#$%^&*()_+№ёЁ`~ ”“\"" \
                    "\n\t":
            data = data.replace(i, '')
    print(data)
    #text1 = text(image, 150)
    #print(text1)
    f = open('text.txt', 'w')
    f.write(data)
    f.close()

root = Tk()
var1 = IntVar()
var2 = IntVar()
var3 = IntVar()
var4 = IntVar()
label1 = Label(text="Выберите параметры", height=3)
label1.pack()
c1 = Checkbutton(root, text='Русский', variable=var1, onvalue=1, offvalue=0)
c1.pack()
c2 = Checkbutton(root, text='English', variable=var2, onvalue=1, offvalue=0)
c2.pack()
#c3 = Checkbutton(root, text='Распознавать цифры', variable=var3, onvalue=1, offvalue=0)
#c3.pack()
c4 = Checkbutton(root, text='Фото', variable=var4, onvalue=1, offvalue=0)
c4.pack()
c5 = Checkbutton(root, text='Скрин/картинка', variable=var4, onvalue=0, offvalue=1)
c5.pack()
btn = Button(text="Готово", command=run)
btn.pack()

root.mainloop()

#новейшая бета версия