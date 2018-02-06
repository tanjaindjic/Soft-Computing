import numpy as np
import cv2
import os

def cropNotes(path):
    #TESTIRAMO NA OVOJ SLICI PREPOZNAVANJE REDOVA NOTNOG SISTEMA
    if path=="":
        return
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    minLineLength = int(img.shape[1] *0.8)
    lines = cv2.HoughLinesP(image=edges, rho=0.02, theta=np.pi / 500, threshold=5, lines=np.array([]),
                                minLineLength=minLineLength, maxLineGap=30)

    y, x, c = lines.shape
    matrix = []
    #BOJIMO LINIJE U REDOVIMA NOTNOG SISTEMA DA VIDIMO KOJE JE IZDVOJIO
    for i in range(y):
            cv2.line(img, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 1, cv2.LINE_AA)

       # cv2.imshow('edges', edges)
    cv2.imshow('result', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #BRISEMO SVE OSIM TIH LINIJA KOJE JE PREPOZNAO, RADI BOLJE PREGLEDNOSTI
    for col in range(img.shape[1]):
        for row in range(img.shape[0]):
            if (img.item(row, col, 2) != 255):
                img.itemset((row, col, 0), 255)
                img.itemset((row, col, 1), 255)
                img.itemset((row, col, 2), 255)

    cv2.imshow('result', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #PRAVIMO MATRICU POZICIJA HORIZONTALNIH LINIJA
    col = img.shape[1] / 2
    col = int(col)
    for row in range(img.shape[0]):

        if (img.item(row, col, 2) == 255 and img.item(row, col, 0) < 230 and img.item(row, col, 1) < 230):
            if (img.item(row - 1, col, 2) > 230 and img.item(row - 1, col, 0) > 230 and img.item(row - 1, col,
                                                                                                     1) > 230):
                l = [row, col]
                matrix.append(row)
                # img.itemset((row,col, 0), 255)
    #DUZINA JE BROJ LINIJA IZ MATRICE PODELJENO SA 5 JER U SVAKOM REDU NOTNOG SISTEMA IMA PO 5 HORIZONTALNIH LINIJA
    #DOBIJAMO BROJ REDOVA TJ DELOVA KOJE TREBA ISECI I ZATIM POSEBNO OBRADITI
    loc = os.getcwd()
    loc += '/images/parts'
    print(loc)
    fileList = os.listdir(loc)
    for fileName in fileList:
        os.remove(loc + "/" + fileName)
    length = len(matrix) / 5
    length = int(length)
    a =  matrix[1]
    b = matrix[0]
    min_razmak = []
    min_razmak = a - b
    start_razmak = b
    if(b>50):
        start_razmak=50

    #UCITAVAMO SLIKU I DELIMO JE U DELOVE VODECI SE MATRICOM KOJA SADRZI POZICIJE SVIH HORIZONTALNIH LINIJA
    img = cv2.imread(path)
    for i in range(length):
        for j in range(4):
            if (matrix[i*5+1+j]-matrix[i*5+j]<min_razmak):
                min_razmak = matrix[i*5+1+j]-matrix[i*5+j]
        top = matrix[i * 5]
        bottom = matrix[(i * 5) + 4]
        if(bottom-top>min_razmak+20):
            top -=10
            bottom = top + min_razmak*5 + 10
        lajna = img[(top - start_razmak):(bottom + start_razmak), :, :]
        ime  = 'images/parts/slika'
        ime += str(i)
        ime += '.png'
        cv2.imwrite(ime, lajna)
        # for col in range(img.shape[1]):
        #     black=True
        #     for row in range(top, bottom):
        #         if(img.item(row, col, 1) > 100):
        #             black=False
        #     if(black == True):
        #         img.itemset((row, col, 0), 255)
        #         img.itemset((row, col, 1), 255)
        #         img.itemset((row, col, 2), 255)

        cv2.imshow('lajna', lajna)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # BRISEMO STARE SLIKE AKO JE VEC RADJEN OVAJ POSTUPAK

    loc = os.getcwd()
    loc += '/images/notes'
    print(loc)
    fileList = os.listdir(loc)
    for fileName in fileList:
        os.remove(loc + "/" + fileName)
    count = 0
    #PROBA PRVOG DELA SLIKE TJ PRVOG REDA, BRISEMO HORIZONTALNE LINIJE DA IZDVOJIMO SIMBOLE
    for i in range(length):
        img_path = 'images/parts/slika'
        img_path+=str(i)
        img_path+='.png'
        img = cv2.imread(img_path)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        minLineLength = int(img.shape[1] * 0.8)
        lines = cv2.HoughLinesP(image=edges, rho=0.02, theta=np.pi / 500, threshold=10, lines=np.array([]),
                                    minLineLength=minLineLength, maxLineGap=50)

        y, x, c = lines.shape
        matrix = []
            # print(lines.shape)
        for i in range(y):
             cv2.line(img, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (255, 255, 255), 2,
                    cv2.LINE_AA)

        for row in range(img.shape[0]):
            for col in range(img.shape[1]):
                if (img.item(row, col, 2) < 100):
                    if (img.item(row - 1, col, 2) < 100):
                        if (matrix.__contains__(col)):
                            continue
                        else:
                            matrix.append(col)
                        # img.itemset((row,col, 0), 255)
        matrix.sort()

        #ODVAJAMO NOTE
        notes = []
        matSize = len(matrix) - 1
        begin = matrix[0] - 1
        for i in range(matSize):
            if (matrix[i + 1] - matrix[i] > 5):
                end = matrix[i]
                l = [begin, end]
                notes.append(l)
                begin = matrix[i + 1]

            # print notes

        cv2.imshow('lines', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        length1 = len(notes)


        #OD ORIGINALNE SLIKE IZDVAJAMO NOTE I SVAKU SECEMO U POSEBNU SLIKU
        img = cv2.imread(img_path)
        for j in range(length1):
            value = notes[j]
            left = value[0]
            right = value[1]
            notica = img[:, (left - 15):(right + 15), :]
            ime = 'images/notes/nota'
            ime += str(count)
            ime += '.png'
            gray_image = cv2.cvtColor(notica, cv2.COLOR_BGR2GRAY)
       #     notica =  cv2.bitwise_not(gray_image)
            cv2.imwrite(ime, notica)
            count+=1
