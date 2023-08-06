from helper_functions import annotate_images, apply_transformations, calculate_ssim

# transformations = { "compress": [25,50,75,90], 
#                     "removal" : True        }
# webpage = Folder address that must contain an HTML file
# weighted SSIM = ["imageID":{   
#                             "src": ".\link.jpg"
#                             "compress_25": 0.915,
#                             "compress_50": 0.80,
#                             "removal" : 0.0       }]
def get(webpage,transformations):
    try:
        images = annotate_images(webpage)
        new_images,transformed_webpages = apply_transformations(transformations,webpage,images)
        weighted_ssim = calculate_ssim(new_images,transformed_webpages)
        return beautify_result(images, transformations, weighted_ssim)
    except Exception as e:
        print("Error: Please make sure you are following the correct syntax.")
        print(e)

def beautify_result(images,transformations,data):
    # {
    #     ID: {
    #             src : '',
    #             compress_25 : 0.9,
    #             compress_50 : 0.8,
    #             remove      : 0.9,
    #         },
    # }

    result = {}
    for eachImage in images:
        result[eachImage] = {}
        result[eachImage]["src"] = images[eachImage]
        for compression in transformations["compress"]:
            result[eachImage]["compress_"+ str(compression)] = data["compress_"+eachImage+"_" + str(compression)]["WMSSIM"]
        if transformations["removal"]:
            result[eachImage]["remove"] = data["remove_"+eachImage]["WMSSIM"]
    return result