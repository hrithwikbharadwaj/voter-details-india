from PyPDF2 import PdfWriter, PdfReader
import cv2
from pdf2image import convert_from_path
import numpy as np
import os
import io
from google.cloud import vision
import pandas as pd
import warnings
import requests
import math

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'keys.json'

IMAGE_DPI = 150


def convertArraytoBytes(array):
    success, encoded_image = cv2.imencode('.png', array)
    return encoded_image.tobytes()


def extractThreeNearestPages(pdf_path, mini_pdf_path):
    reader = PdfReader(pdf_path)
    totalPages = reader.numPages
    writer = PdfWriter()
    pageRange = math.ceil(665/30) + 1
    previousPageIndex = pageRange - 1
    currentPageIndex = pageRange
    nextPageIndex = pageRange + 1

    # if previousPageIndex <= totalPages:
    #     writer.add_page(reader.pages[previousPageIndex])
    if currentPageIndex <= totalPages:
        writer.add_page(reader.pages[currentPageIndex])
    if nextPageIndex <= totalPages:
        writer.add_page(reader.pages[nextPageIndex])

    with open(mini_pdf_path, "wb") as fp:
        writer.write(fp)


def get_text_from_pdf(pdf_path, mini_pdf_path, locale_path) -> str:
    extractThreeNearestPages(pdf_path, mini_pdf_path)
    reader = PdfReader(mini_pdf_path)
    totalpages = reader.numPages
    client = vision.ImageAnnotatorClient()

    if os.name == 'nt':
        pages = convert_from_path(
            mini_pdf_path, IMAGE_DPI, poppler_path=r"C:\Program Files\poppler-0.68.0_x86\bin")
    else:
        pages = convert_from_path(mini_pdf_path, IMAGE_DPI)

    page_no = 0
    j = 0

    for page in pages:

        page_no = page_no+1

        if(page_no > totalpages):
            break
        # console_file.write('hello ' + str(i))

        # page.save('page'+str(i)+'.jpg', 'JPEG')
        image = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

        # image = cv2.imread('page'+str(i)+'.jpg')
        original = image.copy()
        headerImage = original[50:80, 0:900]
        # file = open("testImage.png", "wb")
        # file.write(headerImage)
        # file.close()
        # save headerImage
        headerImageBytes = convertArraytoBytes(headerImage)
        headerRequestImage = vision.Image(content=headerImageBytes)
        headerImageResponse = client.text_detection(image=headerRequestImage)
        # split after :
        if(headerImageResponse.text_annotations.__len__() > 0):
            headerText = headerImageResponse.text_annotations[0].description.split(":")[
                1]
            headerText = headerText.lstrip()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV)[1]

        cnts = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        image_number = 0
        min_area = 3000

        for c in cnts:
            area = cv2.contourArea(c)
            if area > min_area:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(original, (x, y),
                              (x + w, y + h), (36, 255, 12), 2)

                img_list = []

                if(h < 157):

                    row1 = original[y:y+h, x:x+379]
                    row2 = original[y:y+h, x+380:x+756]
                    row3 = original[y:y+h, x+757:x+1133]
                    for i in range(3):
                        img_list.append(convertArraytoBytes(
                            array=eval('row'+str(i+1))))

                else:
                    row1 = original[y:y+157, x:x+379]
                    row2 = original[y:y+157, x+380:x+756]
                    row3 = original[y:y+157, x+757:x+1133]
                    row4 = original[y+157:y+h, x:x+379]
                    row5 = original[y+157:y+h, x+380:x+756]
                    row6 = original[y+157:y+h, x+757:x+1133]

                    for i in range(6):
                        img_list.append(convertArraytoBytes(
                            array=eval('row'+str(i+1))))

                for content in img_list:
                    image = vision.Image(content=content)

                    response = client.text_detection(image=image)
                    df = pd.DataFrame(columns=['locale', 'description'])

                    texts = response.text_annotations
                    for text in texts:
                        text.description = text.description + "\n" + "address: " + headerText
                        df = df.append(
                            dict(
                                locale=text.locale,
                                description=text.description
                            ),
                            ignore_index=True
                        )
                    try:
                        with open(locale_path, "a", encoding='utf-8') as myfile:
                            myfile.write(df['description'][0])
                            myfile.write("\n------------\n")
                    except:
                        pass
                j = j+1


def get_pdf_from_url(url):
    response = requests.get(url, verify=False, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
    return response.content


def savePDF(url, PDFPath):
    if not os.path.exists(PDFPath):
        pdf = get_pdf_from_url(url)
        with open(PDFPath, 'wb') as f:
            f.write(pdf)
