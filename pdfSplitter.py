import math
from PyPDF2 import PdfWriter, PdfReader
PDFPATH = f'temp/S10A217P51.pdf'
PDF2Path = f'temp/sample2.pdf'

reader = PdfReader(PDFPATH)
# writer = PdfWriter()
# print(reader.numPages)
# totalPages = reader.numPages
# pageRange = math.ceil(665/30) + 1


def extractThreeNearestPages(reader, mini_pdf_path):
    totalPages = reader.numPages
    writer = PdfWriter()
    pageRange = math.ceil(665/30) + 1
    previousPageIndex = pageRange - 1
    currentPageIndex = pageRange
    nextPageIndex = pageRange + 1

    if previousPageIndex <= totalPages:
        writer.add_page(reader.pages[previousPageIndex])
    if currentPageIndex <= totalPages:
        writer.add_page(reader.pages[currentPageIndex])
    if nextPageIndex <= totalPages:
        writer.add_page(reader.pages[nextPageIndex])

    with open(mini_pdf_path, "wb") as fp:
        writer.write(fp)


extractThreeNearestPages(reader, PDF2Path)
