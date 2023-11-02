import pytesseract
import cv2

image = cv2.imread("data/jj.png")

base_image = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imwrite("resume/jj_gray.png", gray)

blur = cv2.GaussianBlur(gray, (7,7), 0)

cv2.imwrite("resume/jj_blur.png", blur)

thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

cv2.imwrite("resume/jj_thresh.png", thresh)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))

cv2.imwrite("resume/jj_kernel.png", kernel)

dilate = cv2.dilate(thresh, kernel, iterations=1)

cv2.imwrite("resume/jj_dilate.png", dilate)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cnts = cnts[0] if len(cnts) == 2 else cnts[1]

# organize this contours from left to right
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0]) 

results = []
for c in cnts:
    x, y, width, height = cv2.boundingRect(c)
    if height > 200 and width > 20:
        roi = image[y:y + height, x: x + height]
        cv2.imwrite("resume/jj_roi.png", roi)
        # start from x stretch til width, from y stretch til height, color
        cv2.rectangle(image, (x, y), (x+width, y+height), (36, 255, 12), 2)
        ocr_result = pytesseract.image_to_string(roi)
        ocr_result = ocr_result.split("\n")
        for item in ocr_result:
            results.append(item)

cv2.imwrite("resume/jj_bbox.png", image)

print(results)