import os


def getCaptchaHeaders():
    return {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,ta;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'Electoral=456c656374726f6c7365617263682d73657276957234; Electoral=456c656374726f6c7365617263682d73657276957234; cookiesession1=678B2867FFB16F1E02B1283C8A931300; runOnce=true; electoralSearchId=xetigxgmpvlzqmcefwlcw1hk; __RequestVerificationToken=FCwqEXXu4x5T37b7yfzBS56V7gSVKz8twSo-2QzOm36kr9bPALSRGxakDfRKPcEgqhTef3acSLBbDqNwaDgxEwQkuAwgVMMKvZHlbem8pDk1',
        'Referer': 'https://electoralsearch.in/',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }


def getVoterPayload(name, dob, relationName, gender, txtCaptcha):
    payload = {
        "txtCaptcha": txtCaptcha,
        "search_type": "details",
        "reureureired": "ca3ac2c8-4676-48eb-9129-4cdce3adf6ea",
        "name": name,
        "rln_name": relationName,
        "page_no": 1,
        "location": "S10,,",
        "results_per_page": 10,
        "location_range": "20",
        "age": None,
        "dob": dob,
        "gender": gender
    }
    return payload


def createTempDir():
    if not os.path.exists("temp"):
        os.makedirs("temp")


def getPDFURL(acNumber, fileName):

    url = f"https://ceo.karnataka.gov.in/finalroll_2022/Kannada/MR/AC{acNumber}/{fileName}"
    return url


def getFileName(stateCode, partNumber, acNumber):
    if(stateCode == "S10"):
        return f"{stateCode}A{acNumber}P{partNumber}.pdf"


def validateStringNotEmpty(value, data):
    if value not in data:
        message = value + " cannot be null or undefined"
        return message, 400
    if len(data[value]) <= 0:
        message = value + " cannot be empty"
        return message, 400
