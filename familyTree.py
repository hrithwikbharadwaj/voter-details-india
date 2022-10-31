import re


def getKeyValue(str):
    properties = {}
    something = str.split(":")
    if len(something) > 2:
        allValues = str.split(" ")
        values = allValues[2::3]
        keys = allValues[0::3]
        for index, value in enumerate(values):
            properties[keys[index]] = value
        return properties
    key = something[0].strip()
    match = re.search("^House", key)
    if(match):
        key = "houseNumber"
    value = something[len(something) - 1].strip()
    properties[key] = value
    return properties


def removeBlankSpaces(lines):
    while("" in lines):
        lines.remove("")


def findMember(ssno, members):
    for member in members:
        if(member["ssno"] == ssno):
            return member
    return False


def findFamilyMembers(houseNumber, members):
    family = []
    for member in members:
        if(member["houseNumber"] == houseNumber):
            family.append(member)
    return family


def get_all_people_data(serialNumber, english_path: str):
    with open(english_path, encoding="utf8") as f:
        content = f.read()
    blocks = content.split('------------')
    members = []
    # presentBlock = blocks[0]

    for block in blocks:
        lines = block.split('\n')
        removeBlankSpaces(lines)
        for value in lines:
            if(re.search('^[0-9]+', value)):
                ssno = re.search('[0-9]+', value).group(0)
                members.append({"ssno": ssno})
            memberValue = members[len(members) - 1]
            memberValue.update(getKeyValue(value))
    user = findMember(serialNumber, members)
    houseNumber = user["houseNumber"]
    family = findFamilyMembers(houseNumber, members)
    return family


# get_all_people_data(
#     "665", "temp-c1a07dbe-5893-11ed-9098-3e9509a4dc49\englishText.txt")
