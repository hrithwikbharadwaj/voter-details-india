import re


def getKeyValue(str):
    properties = {}
    attributes = str.split(":")
    # if there are multiple attributes in one line then form a dict and return it
    if len(attributes) > 2:
        allValues = str.split(" ")
        values = allValues[2::3]
        keys = allValues[0::3]
        for index, value in enumerate(values):
            properties[keys[index]] = value
        return properties
    key = attributes[0].strip()
    match = re.search("^House", key)
    if(match):
        key = "houseNumber"
    value = attributes[len(attributes) - 1].strip()
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
        if "houseNumber" in member:
            if(member["houseNumber"] == houseNumber):
                family.append(member)
    return family


def get_all_people_data(serialNumber, english_path: str):
    with open(english_path, encoding="utf8") as f:
        content = f.read()
    blocks = content.split('------------')
    members = []

    for block in blocks:
        lines = block.split('\n')
        removeBlankSpaces(lines)
        for index, value in enumerate(lines):
            if index < len(lines) - 1:
                if re.search('^House', lines[index+1]):
                    if "Father's Name" in memberValue:
                        memberValue["Father's Name"] = memberValue["Father's Name"] + " " + value
                    if "Husband's Name" in memberValue:
                        memberValue["Husband's Name"] = memberValue["Husband's Name"] + " " + value

            if(re.search('^[0-9]+', value)):
                ssno = re.search('[0-9]+', value).group(0)
                members.append({"ssno": ssno})
            memberValue = members[len(members) - 1]
            memberValue.update(getKeyValue(value))
    user = findMember(serialNumber, members)
    houseNumber = user["houseNumber"]
    family = findFamilyMembers(houseNumber, members)
    return family
