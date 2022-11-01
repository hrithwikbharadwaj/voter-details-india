from fuzzy import levenshtein_ratio_and_distance


def getSampleData():
    return [
        {
            "Age": "92",
            "Available": "Available",
            "Father's Name": "",
            "Gender": "Male",
            "Name": "Shama",
            "address": "1-Revenue Houses belonging to Kidagannamma Barangay, Hebbalu 1st Phase, , Railway",
            "houseNumber": "109",
            "ssno": "585"
        },
        {
            "Age": "88",
            "Gender": "Female",
            "Husband's Name": "Shama",
            "Name": "Sharada",
            "houseNumber": "109",
            "ssno": "583"
        },
        {
            "Age": "56",
            "Father's Name": "Shama",
            "Gender": "Male",
            "Name": "Sridhar",
            "houseNumber": "109",
            "ssno": "58s"
        },
        {
            "Age": "67",
            "Father's Name": "Shama",
            "Gender": "Male",
            "Name": "Viji",
            "houseNumber": "109",
            "ssno": "50s"
        },
        {
            "Age": "50",
            "Gender": "Female",
            "Husband's Name": "Viji",
            "Name": "Geetha",
            "houseNumber": "109",
            "ssno": "50ss"
        },
        {
            "Age": "47",
            "Gender": "Female",
            "Husband's Name": "Sridhar",
            "Name": "Lakshmi",
            "houseNumber": "109",
            "ssno": "656"
        }
    ]


def locateElement(children, name):
    for element in children:
        if(element["Name"] == name):
            return element

        if "children" in element:
            some = locateElement(element["children"], name)
            if(some):
                return some


def fuzzyLocateElement(children, name):
    for element in children:
        if(levenshtein_ratio_and_distance(element["Name"], name) <= 6):
            return element

        if "children" in element:
            some = locateElement(element["children"], name)
            if(some):
                return some


def locateElementAndParent(children, name):
    for element in children:
        if(element["Name"] == name):
            return element
        if "children" in element:
            some = locateElementAndParent(element["children"], name)
            if(some):
                return {"element": some, "parent": element}


def fuzzyLocateElementAndParent(children, name):
    for element in children:
        if(levenshtein_ratio_and_distance(element["Name"], name) <= 6):
            return element
        if "children" in element:
            some = fuzzyLocateElementAndParent(element["children"], name)
            if(some):
                return {"element": some, "parent": element}


def convertAgeToNumber(elements):
    for element in elements:
        element["Age"] = int(element["Age"])


def getFamilyTree(data):
    convertAgeToNumber(data)
    ageSortedData = sorted(data, key=lambda x: x["Age"], reverse=True)
    familyTree = []
    for element in ageSortedData:
        if "Father's Name" in element:
            if(len(element["Father's Name"])):
                father = locateElement(familyTree, element["Father's Name"])
                if not father:
                    familyTree.append(element)
                else:
                    if "children" in father:
                        father["children"].append(element)
                    else:
                        father["children"] = [element]

            else:
                familyTree.append(element)
        if "Husband's Name" in element:
            elementAndParent = locateElementAndParent(
                familyTree, element["Husband's Name"])
            if(elementAndParent):
                if "element" in elementAndParent:
                    elementAndParent["element"]["wife"] = element
                else:
                    elementAndParent["wife"] = element
    return familyTree


def getFamilyTreeWithFuzzySearch(data):
    convertAgeToNumber(data)
    ageSortedData = sorted(data, key=lambda x: x["Age"], reverse=True)
    familyTree = []
    for element in ageSortedData:
        if "Father's Name" in element:
            if(len(element["Father's Name"])):
                father = fuzzyLocateElement(
                    familyTree, element["Father's Name"])
                if not father:
                    familyTree.append(element)
                else:
                    if "children" in father:
                        father["children"].append(element)
                    else:
                        father["children"] = [element]

            else:
                familyTree.append(element)
        if "Husband's Name" in element:
            elementAndParent = fuzzyLocateElementAndParent(
                familyTree, element["Husband's Name"])
            if(elementAndParent):
                if "element" in elementAndParent:
                    elementAndParent["element"]["wife"] = element
                else:
                    elementAndParent["wife"] = element
    return familyTree


# print(getFamilyTree(getSampleData()))
