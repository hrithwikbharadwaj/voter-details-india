from utils import getCaptchaHeaders, getVoterPayload
from captcha import solveCaptcha
import requests


def writeCaptchaToDisk(captcha, captchaPath):
    file = open(captchaPath, "wb")
    file.write(captcha)
    file.close()


def generateCaptchaImage(headers):
    response = requests.get(
        'https://electoralsearch.in/Home/GetCaptcha?image=true', headers=headers)
    return response.content


def getVoterInfo(name, dob, gender, relationName, captchaPath):
    MAX_TRIES = 20
    response = None
    while MAX_TRIES > 0:
        print(MAX_TRIES)
        headers = getCaptchaHeaders()
        captchaImage = generateCaptchaImage(headers)

        writeCaptchaToDisk(captchaImage, captchaPath)

        captchaText = solveCaptcha(captchaPath).strip()
        requestData = getVoterPayload(
            name, dob, relationName, gender, captchaText)
        cookies = {
            'Electoral': '456c656374726f6c7365617263682d73657276657234',
            'Electoral': '456c656374726f6c7365617263682d73657276657234',
            'cookiesession1': '678B2867FFB16F1E02B1283C8A931300',
            'runOnce': 'true',
            'electoralSearchId': 'xetigxgmpvlzqmcefwlcw1hk',
            '__RequestVerificationToken': 'FCwqEXXu4x5T37b7yfzBS56V7gSVKz8twSo-2QzOm36kr9bPALSRGxakDfRKPcEgqhTef3acSLBbDqNwaDgxEwQkuAwgVMMKvZHlbem8pDk1',
        }
        headers["Accept"] = 'application/json, text/plain, */*'
        headers["Accept-Language"] = 'en-US,en;q=0.9,ta;q=0.8'
        response = requests.post('https://electoralsearch.in/Home/searchVoter',
                                 headers=headers, cookies=cookies, json=requestData)

        if response.text == 'Wrong Captcha':
            print(response.text)
            MAX_TRIES = MAX_TRIES - 1
        else:
            break

    if MAX_TRIES == 0:
        print("Max Tries Reached. Try Again")
        return None
    docs = response.json()["response"]["docs"]
    if len(docs) == 0:
        print("No results found")
        return None
    return docs[0]
