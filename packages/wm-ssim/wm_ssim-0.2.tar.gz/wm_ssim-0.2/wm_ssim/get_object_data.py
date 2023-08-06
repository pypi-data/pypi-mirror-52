#This script returns a json file containing dimensions and location for all images in the web pages it
#is given. It also returns dimensions for the web page body

# output json format:  
# {filename1:
# 	{'imgs':
# 		{img1:{height:1,width:1,area:1,xloc:20,yloc:400},img2:{height:2,width:2,area:4,xloc:412,yloc:213},...}
# 	'body': {height:10,width:10,area:100}
# 	},
#  filename2: ...
# }

import sys
import util
from selenium import webdriver
import getopt
import os
import json
from pyvirtualdisplay import Display


def setup_driver():
    driver = webdriver.Firefox(executable_path='/home/ab/geckodriver')
    driver.maximize_window()
    return driver

def get_page_img_dims(filepath,filename_nx):
    with Display():
        sizes_dict = {}
        driver = setup_driver()
        abs_path = util.filepath_for_browser(filepath)
        sizes_dict[filename_nx] = {'imgs':{}}
        driver.get(abs_path)
        body_tag = driver.find_element_by_tag_name('body')
        img_tags = driver.find_elements_by_tag_name('img')

        body_dims = body_tag.size
        body_dims['area'] = body_tag.size['width'] * body_tag.size['height']
        sizes_dict[filename_nx]['body'] = body_dims
        for tag in img_tags:
            try:
                img_name = tag.get_attribute('src').split("/")[-1]
                if not img_name:
                    img_name = tag.get_attribute('src').split("/")[-2]
                img_name_nx = util.filename_no_ext(img_name)
                dims = tag.size
                dims['area'] = tag.size['width'] * tag.size['height']
                sizes_dict[filename_nx]['imgs'][img_name_nx] = dims
                sizes_dict[filename_nx]['imgs'][img_name_nx]['xloc'] = tag.location['x']
                sizes_dict[filename_nx]['imgs'][img_name_nx]['yloc'] = tag.location['y']
                sizes_dict[filename_nx]['imgs'][img_name_nx]['src'] = img_name

            except:
                driver.quit()
                continue

        driver.quit()
        import copy
        return copy.deepcopy(sizes_dict[filename_nx])
