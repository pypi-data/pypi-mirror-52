import string
import os
from bs4 import BeautifulSoup
import shutil
from compress import compress_image_by_percentage as compress
import copy
from PIL import Image
import numpy as np
from get_object_data import get_page_img_dims as getImageDimensions
from skimage import measure
import cv2

temp_folder = "tmp"
shouldReplace = False

def annotate_images(webpageFolder):
    images = {}
    ids =  list(string.ascii_uppercase+string.ascii_lowercase)
    webpage = filter(lambda x: ".html" in x,os.listdir(webpageFolder))
    assert(len(webpage) ==1)
    webpage = webpage[0]
    i = 0
    html_code = ""

    # annotate eah image with a unique ID
    with open(os.path.join(webpageFolder,webpage), "r") as f:
        soup = BeautifulSoup(f.read(),"lxml")
        for each_img in soup.findAll("img"):
            each_img['id'] = ids[i]
            i += 1
            images[each_img['id']] = each_img['src']
        html_code = soup.prettify("utf-8")
    
    # save webpage with updated image ID's
    with open(webpage,"w") as f:
        f.write(html_code)
    return images

def apply_transformations(transformations,webpageFolder,images):
    # Create a tmp fodler and copy original HTML and images to that folder
    os.mkdir(temp_folder)
    webpage = filter(lambda x: ".html" in x,os.listdir(webpageFolder))[0]
    webpage_comple = os.path.join(webpageFolder,webpage)
    shutil.copy(webpage_comple,os.path.join(temp_folder,"original.html"))

    new_images = {}
    for id in images:
        src = images[id]
        image_name = src.split("/")[-1]
        if image_name == "":
            image_name = src.split("/")[-2]
        new_images[id] = image_name
        shutil.copy(src, os.path.join(temp_folder,image_name))
    
    #Make all transformed Images in tmp folder
    images_names = filter(lambda x: x.split(".")[1] != "html" ,os.listdir(temp_folder))
    for eachImage in images_names:
        for percReduction in transformations["compress"]:
            newName = eachImage.split(".")[0] + "_"+str(percReduction) +"."+ eachImage.split(".")[-1]
            compress(temp_folder,temp_folder,eachImage,newName,percReduction)
    

    # Make a dict of all transformations
    folders = {}
    folders["original"] = new_images.keys()

    for id in images:
        for percReduction in transformations["compress"]:
            fname = "compress_" + id + "_" + str(percReduction)
            if fname not in folders.keys():
                folders[fname] = []
            newName = images[id].split("/")[-1]
            if newName == "":
                newName = images[id].split("/")[-2]
            newName_src = newName.split(".")[0] + "_"+str(percReduction) +"."+  images[id].split(".")[-1]
            newName_id  = id + "_" + str(percReduction) 
            new_images[newName_id] = newName_src
            
            folders[fname].append(newName_id)
            for j in images:
                if j != id:
                    folders[fname].append(j)
    
    if transformations["removal"]:
        #Generate White Images corresponding to original Images
        for id in images:
            generateWhiteImage(images[id],temp_folder,images[id].split("/")[-1].split(".")[0])
        
        for id in images:
            name = "remove_" + id
            folders[name] = [name]
            new_images[name] =  images[id].split("/")[-1].split(".")[0]+"_removal.jpg"
            for otherImage in images:
                if otherImage != id:
                    folders[name].append(otherImage)


    #Create folders Now
    for eachFolder in folders:
        if not os.path.exists(os.path.join(temp_folder,eachFolder)):
            os.mkdir(os.path.join(temp_folder,eachFolder))
        for eachFile in folders[eachFolder]:
            shutil.copy( os.path.join(temp_folder,new_images[eachFile]), os.path.join(temp_folder, eachFolder,new_images[eachFile]))
        
    # Create HTML files
    for eachFolder in folders:
        with open(os.path.join(temp_folder,"original.html"), "r") as f:
            soup = BeautifulSoup(f.read(),"lxml")
            for each_img in soup.findAll("img"):
                img_id = filter(lambda x: each_img["id"] + "_" in x or "_"+each_img["id"] in x or each_img["id"] == x , folders[eachFolder])[0]
                each_img['src'] = new_images[img_id]
            html_code = soup.prettify("utf-8")
            with open(os.path.join(temp_folder,eachFolder,eachFolder+".html"), "w") as new_f:
                new_f.write(html_code)

    return new_images,folders

def calculate_ssim(images,transformed_webpages):
    final_data = {}
    for eachFile in transformed_webpages:
        data = getImageDimensions(os.path.join(temp_folder,eachFile,eachFile+".html"),eachFile+".html")
        final_data[eachFile] = data
    
    final_data = add_ssim_to_data(final_data)

    for eachPage in final_data:
        final_data[eachPage]["WMSSIM"] =  calculateWeightedMeanSSIM(final_data[eachPage])
    clear_tmp_folder()
    return final_data


def generateWhiteImage(image, imagesFolder,id):
    with Image.open(image) as img:
        width, height = img.size

    img = np.zeros([height,width,3],dtype=np.uint8)
    img.fill(255)
    im = Image.fromarray(img)
    im.save(os.path.join(imagesFolder,id+"_removal.jpg"))
    return

def clear_tmp_folder():
    #Delete tmp Folder
    shutil.rmtree(temp_folder)


def add_ssim_to_data(imagesData):
    basePage = "original"
    baseImages = imagesData[basePage]['imgs'].keys()
    baseImages.sort()

    pages = filter(lambda x: x != basePage, imagesData.keys())

    for eachImage in baseImages:
        imagesData[basePage]['imgs'][eachImage]['SSIM'] = 1
    for eachPage in pages:
        for eachImage in baseImages:
            pageImage = filter(lambda x:  eachImage+ "_" in x or "_"+eachImage in x or eachImage == x,  imagesData[eachPage]['imgs'].keys())[0]
            if "remove_" in pageImage and not shouldReplace:
                imagesData[eachPage]['imgs'][pageImage]['SSIM']  = 0
            elif imagesData[eachPage]['imgs'][pageImage]['src'] == imagesData[basePage]['imgs'][eachImage]['src']:
                imagesData[eachPage]['imgs'][pageImage]['SSIM']  = 1
            else:
                imagesData[eachPage]['imgs'][pageImage]['SSIM'] = find_ssim(imagesData[eachPage]['imgs'][pageImage]['src'], imagesData[basePage]['imgs'][eachImage]['src'], temp_folder)
    return imagesData

def find_ssim(img1, img2, filePath):
    return get_ssim_value(os.path.join(filePath,img1),os.path.join(filePath,img2))

def get_ssim_value(imageA,imageB):
    imageA = cv2.imread(imageA)
    imageB = cv2.imread(imageB)
    H,W,A = imageA.shape
    imageB = cv2.resize(imageB,(W,H))
    s = measure.compare_ssim(imageA,imageB,multichannel=True)
    return s


def calculateWeightedMeanSSIM(pageData):
    WMSSIM = 0
    for eachImage in pageData['imgs'].keys():
        if 'SSIM' in pageData['imgs'][eachImage].keys():
            WMSSIM += weightOfImage(eachImage,pageData)*pageData['imgs'][eachImage]['SSIM']
        else:
            return -1
    return WMSSIM

def weightOfImage(image,pageData):
    return (locationWeightOfImage(image,pageData) + areaWeightOfImage(image,pageData))/2.0


# locW(img1) = dist1/(dist1+dist2+...)
def locationWeightOfImage(image,pageData):
    dist1 = float(pageData['body']['height'] - pageData['imgs'][image]['yloc'])

    totalDist = 0
    for eachImage in pageData['imgs'].keys():
        totalDist += float(pageData['body']['height'] - pageData['imgs'][eachImage]['yloc'])
    
    return dist1/totalDist

# areaW(img1) = area1/(area1+area2+...)
def areaWeightOfImage(image,pageData):
    area1 = float(pageData['imgs'][image]['width'] * pageData['imgs'][image]['height'])

    totalArea = 0
    for eachImage in pageData['imgs'].keys():
        totalArea += float(pageData['imgs'][eachImage]['width'] * pageData['imgs'][eachImage]['height'])
    
    return area1/totalArea