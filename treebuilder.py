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
            "ssno": "663"
        },
        {
            "Age": "88",
            "Gender": "Female",
            "Husband's Name": "Shama",
            "Name": "Sharada",
            "houseNumber": "109",
            "ssno": "664"
        },
        {
            "Age": "56",
            "Father's Name": "Shama",
            "Gender": "Male",
            "Name": "Sridhar",
            "houseNumber": "109",
            "ssno": "665"
        },
        {
            "Age": "67",
            "Father's Name": "Shama",
            "Gender": "Male",
            "Name": "Viji",
            "houseNumber": "109",
            "ssno": "665"
        },
        {
            "Age": "50",
            "Gender": "Female",
            "Husband's Name": "Viji",
            "Name": "Geetha",
            "houseNumber": "109",
            "ssno": "666"
        },
        {
            "Age": "47",
            "Gender": "Female",
            "Husband's Name": "Sridhar",
            "Name": "Lakshmi",
            "houseNumber": "109",
            "ssno": "666"
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


def locateElementAndParent(children, name):
    for element in children:
        if(element["Name"] == name):
            return element
        if "children" in element:
            some = locateElement(element["children"], name)
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
            if "element" in elementAndParent:
                elementAndParent["element"]["wife"] = element
            else:
                elementAndParent["wife"] = element
    return familyTree
