from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import glob 
import matplotlib.pyplot as plt
import skimage.io
import skimage.color
import skimage.filters
import cv2
from skimage.filters import threshold_otsu
from pydantic import BaseModel


class data(BaseModel):
    img1: str
    img2: str

    class Config:
        orm_mode = True

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
def calc(image):
    gray_image = skimage.color.rgb2gray(image)

    # blur the image to denoise
    blurred_image = skimage.filters.gaussian(gray_image, sigma=1.0)

    histogram, bin_edges = np.histogram(blurred_image, bins=256, range=(0.0, 1.0))

    gimg = skimage.color.rgb2gray(image)
    thr = threshold_otsu(gimg)
    binary_mask = blurred_image < thr
    binary_mask1 = blurred_image < 1

    selection = image.copy()
    selection1 = image.copy()
    selection[~binary_mask] = 0
    selection1[~binary_mask1] = 0

    gray = cv2.cvtColor(selection,cv2.COLOR_BGR2GRAY)
    gray1 = cv2.cvtColor(selection1,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY)
    ret, thresh1 = cv2.threshold(gray1,0,255,cv2.THRESH_BINARY)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    area = cv2.countNonZero(thresh)
    area1 = cv2.countNonZero(thresh1)
    per = area*100/area1
    return per

# load image 1
image = skimage.io.imread("D:\MyFiles\git\minor-project-repo\img1.jpeg")
# Load image 2
image2 = skimage.io.imread("D:\MyFiles\git\minor-project-repo\img2.jpeg")

@app.get('/login')
def login(path1:str,path2:str):
    print(path1,path2)

    image1 = skimage.io.imread(path1)

    image2 = skimage.io.imread(path2)

    i1 = calc(image1)
    i2 = calc(image2)

    inc = (i2-i1)*100/i1
    print("An increase of ",inc,"%")
    res=("An increase of ",inc,"%")
    return (res)


