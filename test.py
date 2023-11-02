### Image Preprocessing

from PIL import Image
import cv2
from matplotlib import pyplot as plt

### Open an Image
img_file = "data/diary2.jpg"
img = cv2.imread(img_file)

#cv2.imshow("original image", img) #header is original image
#cv2.waitKey(0) #milliseconds

#display diff image with actual size in matplotlib subplot
def display(img_path):
    dpi = 80
    img_data = plt.imread(img_path)
    height, width, depth = img_data.shape

    #What size does the figure need to be in inches to fit the image
    figsize = width / float(dpi), height / float(dpi)

    #Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    #Hide spines, ticks, etc.
    ax.axis('off')

    #Display the image
    ax.imshow(img_data, cmap='gray')

    plt.show()

def display2(image):
    cv2.imshow("original image", image) #header is original image
    cv2.waitKey(0) #milliseconds

#display(img_file)

### end of Open Image

### Invert Image
inverted_img = cv2.bitwise_not(img)
cv2.imwrite("temp/inverted.jpg", inverted_img)

### end of Invert Image

### Rescaling

### end of rescaling

### Binarization
# convert image into grayscale file
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray_img = grayscale(img)
cv2.imwrite("temp/gray.jpg", gray_img)

#pdf scanning format
thresh, im_bw = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
cv2.imwrite("temp/bw_image.jpg", im_bw)

### end of binarization


### Noise Removal
def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return image

no_noise = noise_removal(im_bw)
cv2.imwrite("temp/no_noise.jpg", no_noise)

### end of noise removal

### dilation and erosion
def thin_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image

eroded_image = thin_font(no_noise)
cv2.imwrite("temp/eroded_image.jpg", no_noise)


def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image

dilated_image = thick_font(no_noise)
cv2.imwrite("temp/dilated_img.jpg", dilated_image)

### end of erosion/dilation


### Rotating and Deskewing
new = cv2.imread("data/slanted_diary2.jpg")
#https://becominghuman.ai/how-to-automatically-deskew-straighten-a-text-image-using-opencv-a0c30aed83df
import numpy as np

def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle
# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)

fixed = deskew(new)
cv2.imwrite("temp/rotated_fixed.jpg", fixed)

### end of rotating/ deskewing


### remove border

def remove_borders(image):
    contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
    cnt = cntsSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return (crop)

no_borders = remove_borders(no_noise)
cv2.imwrite("temp/no_borders.jpg", no_borders)

### end of removing border


### missing border
color = [255, 255, 255]
top, bottom, left, right = [150]*4

image_with_border = cv2.copyMakeBorder(no_borders, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
cv2.imwrite("temp/image_with_border.jpg", image_with_border)

### end of missing border