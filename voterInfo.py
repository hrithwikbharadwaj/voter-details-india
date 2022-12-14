from utils import getCaptchaHeaders, getVoterPayload, getCookies
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
        cookies = getCookies()
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
