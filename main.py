#!/usr/bin/env python3

# import beautifulsoup4
from email.policy import default
from importlib.resources import path
from bs4 import BeautifulSoup
import requests
import argparse
parser=argparse.ArgumentParser()
default_link='https://cs300-www.cs.wisc.edu/wp/wp-content/uploads/2020/12/fall2022/p7/javadocs/ListingMode.html'
parser.add_argument('--output', type=bool,default=True, help="Redirect stdout to java file with class name.")
parser.add_argument('--link', type=str, required=False,
                    default=default_link,
                    help=f'link to extract code. Will be {default_link} by default')
args = parser.parse_args()


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
    array = array.replace("\r","")
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
page = requests.get(args.link)
# soup = BeautifulSoup(open("./Intersection.html"), "html.parser")
soup = BeautifulSoup(page.text, "html.parser")

className = soup.title.string

if args.output:
    import sys
    import os
    out_path=os.path.join(os.getcwd(),className)+'.java'
    print(f"print code extracted from {args.link} to {out_path}")
    sys.stdout=open(out_path,'w')

className=className.lower()

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
classDescription = class_java.find("div", {"class": className})

# Alternative place of class-description
if classDescription is None:
    #ignore line break token <br>
    for linebreak in class_java.find_all('br'):
        linebreak.extract()
    classDescription = class_java.find("div", {"class": "block"})
    
if classDescription.string!=None:
    classDescription = classDescription.string#why is this NoneType while classDescription is the correct string?
else:
    pass
classDescription = parse(classDescription)

# Make the javadocs for class
print(create_javadocs(classDescription, 0))

# Make the class
print(classHeader + " {\n") 

#
# Get the instance fields
#
instanceFields = main.find("section", {"class": "details"}).find("section", {"id": "field-detail"})
      
if instanceFields is not None:
    instanceFields = instanceFields.find("ul", {"class": "member-list"})

    # Loop through instance fields
    for instanceField in instanceFields.contents:
        # Skip empty lines
        if instanceField == "\n":
            continue

        # Get the field code
        fieldName = instanceField.find("div", {"class": "member-signature"})
        fieldName = squish(fieldName.find_all(text=True))

        # Get the field description
        fieldDescription = squish(instanceField.find("div", {"class": "block"}).find_all(text=True))

        # Make the field
        print("\t" + fieldName + ";" + "\t// " +fieldDescription)

print()

#
# Constructor
#

# Get the constructor
constructor = main.find("section", {"id": "constructor-detail"})

# In case there is no constructor
if constructor is not None:

    # Get the constructor-header
    constructorHeader = constructor.find("div", {"class": "member-signature"}).find_all(text=True)
    constructorHeader = squish(constructorHeader)

    # Get the constructor-description
    constructorDescription = constructor.find("div", {"class": className})
    
    # Alternative case for constructor-description
    if constructorDescription is None:
        constructorDescription = constructor.find("div", {"class": "block"})
    constructorDescription = parse(constructorDescription)

    # Get the constructor parameters
    constructorParameters = constructor.find("dl")

    # In case there is no parameters
    if constructorParameters is not None:
        constructorParameters = parse(constructorParameters.find_all(text=True))
    else:
        constructorParameters = []

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
    loopFunctionDescription = loopFunction.find("div", {"class": className})
    
    # Alternate place of loopFunction-description
    if loopFunctionDescription is None:
        loopFunctionDescription = loopFunction.find("div", {"class": "block"})

    loopFunctionDescription = loopFunctionDescription.find_all(text=True)

    loopFunctionDescription = parse(loopFunctionDescription)

    # Get the loopFunction parameters
    loopFunctionParameters = loopFunction.find("dl")

    # In case function has no parameters
    if loopFunctionParameters is not None:
        loopFunctionParameters = parse(loopFunctionParameters.find_all(text=True))

        # Add @tags to parameters
        loopFunctionParameters = add_tags(loopFunctionParameters)

        # Check if there is override
        override = delete_override(loopFunctionParameters)
    else: 
        loopFunctionParameters = []

    # Print javadocs for loopFunction
    print(create_javadocs(loopFunctionDescription + loopFunctionParameters, 1))

    # Print Override
    if override:
        print("\t@Override")

    # Print loopFunction
    print("\t" + loopFunctionHeader + " {\n" + "\t\t// TODO: Implement\n\t}" + "\n")

print("}")
