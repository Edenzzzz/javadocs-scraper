#!/usr/bin/env python3

# import beautifulsoup4
from bs4 import BeautifulSoup
import requests

# Function to create javadocs from list
def create_javadocs(list, tab):
    javadocs = "\t"*tab + "/**\n"
    for line in list:
        javadocs += "\t"*tab + " * " + line + "\n"
    javadocs += "\t"*tab + " */"
    return javadocs

# Function to squish BS array to single line
def squish(array):
    array = "".join(array)
    array = array.replace("\xa0", " ")
    array = array.replace("\n", "")

    return array

# Function to parse BS Array to list
def parse(array):
    array = "".join(array)
    array = array.replace("\xa0", " ")
    array = array.split("\n")
    array = [x.strip() for x in array]

    return array

# Function to add tags to javadocs description
def add_tags(list):
    tags = ''
    
    # Remove first line if empty
    if list[0] == "":
        list.pop(0)

    i = 0
    while i < len(list):
        # Skip empty lines
        if list[i] == "":
            i += 1
            continue
        
        # Check for parameters
        # Parameters, Returns, Throws
        if list[i] == "Parameters:":
            list.insert(i, "")
            i += 1
            tags = "@param "
        elif list[i] == "Returns:":
            list.insert(i, "")
            i += 1
            tags = "@return "
        elif list[i] == "Throws:":
            list.insert(i, "")
            i += 1
            tags = "@throws "
        else:
            list[i] = tags + list[i]

        i += 1
    
    return list

# Function to delete override tags
def delete_override(list):
    tags = ''
    i = 0
    while i < len(list):
        # Skip empty lines
        if list[i] == "":
            i += 1
            continue
        
        # Check for override
        if list[i] == "Overrides:":
            list.pop(i)
            list.pop(i)
            return True
        else:
            i += 1

    return False

# Set up beautifulsoup4
page = requests.get("https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Object.html")
# soup = BeautifulSoup(open("./Intersection.html"), "html.parser")
soup = BeautifulSoup(page.text, "html.parser")
className = soup.title.string.lower()

# Main part of document:
main = soup.main

# Go to class
class_java = main.find("section", {"id": "class-description"})

# Get the type-signature
typeSignature = class_java.find("div", {"class": "type-signature"})

classHeader = typeSignature.find_all(text=True)
classHeader = "".join(classHeader)
classHeader = classHeader.replace("\n", " ")

# Get the class-description
classDescription = class_java.find("div", {"class": className}).string
classDescription = parse(classDescription)

# Make the javadocs for class
print(create_javadocs(classDescription, 0))

# Make the class
print(classHeader + " {\n") 

#
# Constructor
#

# Get the constructor
constructor = main.find("section", {"id": "constructor-detail"})

# Get the constructor-header
constructorHeader = constructor.find("div", {"class": "member-signature"}).find_all(text=True)
constructorHeader = squish(constructorHeader)

# Get the constructor-description
constructorDescription = constructor.find("div", {"class": className})
constructorDescription = parse(constructorDescription)

# Get the constructor parameters
constructorParameters = constructor.find("dl").find_all(text=True)
constructorParameters = parse(constructorParameters)

# Add @param to parameters
for i in range(len(constructorParameters)):
      if constructorParameters[i] != "" and constructorParameters[i] != "Parameters:":
        constructorParameters[i] = "@param " + constructorParameters[i]

# Print javadocs for constructor
print(create_javadocs(constructorDescription + constructorParameters, 1))

# Print Constructor
print("\t" + constructorHeader + " {\n" + "\t\t// TODO: Implement\n\t}" + "\n")

# 
# Get functions
# 
functions = main.find("section", {"id": "method-detail"}).find("ul", {"class": "member-list"})

# Loop through functions
for loopFunction in functions.contents:

    # skip empty lines
    if loopFunction == "\n":
        continue

    # Get the constructor-header
    loopFunctionHeader = loopFunction.find("div", {"class": "member-signature"}).find_all(text=True)
    loopFunctionHeader = squish(loopFunctionHeader)

    # Get the loopFunction-description
    loopFunctionDescription = loopFunction.find("div", {"class": className}).find_all(text=True)
    loopFunctionDescription = parse(loopFunctionDescription)

    # Get the loopFunction parameters
    loopFunctionParameters = loopFunction.find("dl").find_all(text=True)
    loopFunctionParameters = parse(loopFunctionParameters)

    # Add @tags to parameters
    loopFunctionParameters = add_tags(loopFunctionParameters)
    
    # Check if there is override
    override = delete_override(loopFunctionParameters)

    # Print javadocs for loopFunction
    print(create_javadocs(loopFunctionDescription + loopFunctionParameters, 1))

    # Print Override
    if override:
        print("\t@Override")

    # Print loopFunction
    print("\t" + loopFunctionHeader + " {\n" + "\t\t// TODO: Implement\n\t}" + "\n")

print("}")
