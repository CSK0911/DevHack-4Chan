import re
from pdfminer.high_level import extract_pages, extract_text

programLanguage = ["PYTHON", "JAVA", "JAVASCRIPT", "HTML", "C++", "C#", "PHP"
                   , "RUBY", "KOTLIN", "TYPESCRIPT", "R", "SQL", "JSON", "CSS", "C", "R LANGUAGE", "C LANGUAGE"
                   , "R PROGRAMMING"]

eduLvl = ["FOUNDATION", "DIPLOMA", "BACHELOR", "MASTER", "DOCTOR OF PHILOSOPHY"]

jobList = [
    "INFORMATION TECHNOLOGY",
    "IT",
    "COMPUTER SCIENCE",
    "SOFTWARE ENGINEER",
    "DATA ANALYST",
    "NETWORK ADMINISTRATOR",
    "CYBERSECURITY ANALYST",
    "WEB DEVELOPER",
    "DATABASE ADMINISTRATOR",
    "HEALTHCARE",
    "REGISTERED NURSE",
    "PHYSICIAN",
    "PHARMACIST",
    "PHYSICAL THERAPIST",
    "MEDICAL LABORATORY TECHNICIAN",
    "HEALTHCARE ADMINISTRATOR",
    "FINANCE",
    "FINANCIAL ANALYST",
    "INVESTMENT BANKER",
    "ACCOUNTANT",
    "FINANCIAL ADVISOR",
    "ACTUARY",
    "TAX CONSULTANT",
    "MARKETING",
    "MARKETING MANAGER",
    "DIGITAL MARKETING SPECIALIST",
    "SOCIAL MEDIA MANAGER",
    "MARKET RESEARCH ANALYST",
    "PUBLIC RELATIONS SPECIALIST",
    "CONTENT WRITER",
    "EDUCATION",
    "TEACHER",
    "SCHOOL PRINCIPAL",
    "LIBRARIAN",
    "EDUCATIONAL CONSULTANT",
    "CURRICULUM DEVELOPER",
    "SCHOOL COUNSELOR",
    "ENGINEERING",
    "CIVIL ENGINEER",
    "MECHANICAL ENGINEER",
    "ELECTRICAL ENGINEER",
    "CHEMICAL ENGINEER",
    "AEROSPACE ENGINEER",
    "BIOMEDICAL ENGINEER",
    "SALES",
    "SALES REPRESENTATIVE",
    "ACCOUNT EXECUTIVE",
    "SALES MANAGER",
    "RETAIL SALES ASSOCIATE",
    "BUSINESS DEVELOPMENT MANAGER",
    "INSIDE SALES SPECIALIST",
    "HUMAN RESOURCES",
    "HUMAN RESOURCES MANAGER",
    "RECRUITMENT SPECIALIST",
    "HR GENERALIST",
    "TRAINING AND DEVELOPMENT MANAGER",
    "COMPENSATION ANALYST",
    "EMPLOYEE RELATIONS SPECIALIST",
    "LEGAL",
    "LAW",
    "ATTORNEY",
    "PARALEGAL",
    "LEGAL SECRETARY",
    "JUDGE",
    "LEGAL CONSULTANT",
    "INTELLECTUAL PROPERTY SPECIALIST",
    "CREATIVE ARTS AND DESIGN",
    "GRAPHIC DESIGNER",
    "ILLUSTRATOR",
    "FASHION DESIGNER",
    "VIDEO GAME DEVELOPER",
    "FILM DIRECTOR",
    "PHOTOGRAPHER"
]

emailFormat = ["@gmail"]

### Print Text and find Text

text = extract_text("Resume_JiaJean.pdf")
upText = text.upper()
upText.replace(" ","")
#print(upText)

text2 = extract_text("Resume_JiaJean.pdf").split()
#print(text2)

allText = ""
for text3 in text2:
    allText += text3 + " "

#print(allText)


for lvl in eduLvl:
    if lvl in allText.upper():
        print(lvl)

for jl in jobList:
    if jl in allText.upper():
        print(jl)


pattern = re.compile(r"[a-zA-Z]+,{1}\s{1}")

matches = pattern.findall(text)

names = [n[:-2] for n in matches]
#print(names)




### end of Print Text and find Text

##########

####Extracting image

import fitz #PyMuPDF
from PIL import Image
import io

pdf = fitz.open("Resume_JiaJean.pdf")
counter = 1
for i in range(len(pdf)):
    page = pdf[i]
    images = page.get_images()
    for image in images:
        base_img = pdf.extract_image(image[0])
        #print(base_img)
        image_data = base_img["image"]
        img = Image.open(io.BytesIO(image_data))
        extension = base_img["ext"]
        img.save(open(f"image{counter}.{extension}", "wb"))
        counter += 1

###Extracting Image

#####

### Extracting Tables



#import tabula
#tables = tabula.read_pdf("Resume_JiaJean.pdf", pages="all")
#df = tables[0]
#print(df[df.Age > 30])