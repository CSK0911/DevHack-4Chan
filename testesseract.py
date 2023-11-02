import pytesseract
from PIL import Image

img_file = "data/diary2.jpg"
no_noise = "temp/no_noise.jpg"
newDiary = "data/diary3.png"

img = Image.open(newDiary)

ocr_result = pytesseract.image_to_string(img)

#print(ocr_result)


##########################################################


img2 = "data/paper1.jpg"
img = Image.open(img2)
ocr_result2 = pytesseract.image_to_string(img)
print(ocr_result2)