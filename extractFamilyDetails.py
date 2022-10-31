import requests
import os
import uuid
from utils import createTempDir, getPDFURL, getFileName
from voterInfo import getVoterInfo
from pdfProccessing import savePDF, get_text_from_pdf
from familyTree import get_all_people_data
from translator import translate_locale_out


def start(name, dob, gender, relationName):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'keys.json'

    randomId = uuid.uuid1()

    createTempDir()

    CAPTCHA_PATH = f'temp/{randomId}_captcha.png'
    PDF_PATH = f'temp/voterRoll.pdf'
    LOCAL_TEXT_PATH = f'temp/{randomId}_localText.txt'
    ENGLISH_TEXT_PATH = f'temp/{randomId}_englishText.txt'
    voterInfo = getVoterInfo(name, dob, gender,
                             relationName, CAPTCHA_PATH)
    if(voterInfo == None):
        return "Records Not Found", 400
    fileName = getFileName(voterInfo["st_code"],
                           voterInfo["ps_no"], voterInfo["ac_no"])
    PDF_PATH = f'temp/{fileName}'
    pdfUrl = getPDFURL(voterInfo["ac_no"], fileName)
    savePDF(pdfUrl, PDF_PATH)
    get_text_from_pdf(PDF_PATH, LOCAL_TEXT_PATH,
                      int(voterInfo["slno_inpart"]))
    translate_locale_out(LOCAL_TEXT_PATH, ENGLISH_TEXT_PATH)
    family = get_all_people_data(
        voterInfo["slno_inpart"], ENGLISH_TEXT_PATH)
    return family
