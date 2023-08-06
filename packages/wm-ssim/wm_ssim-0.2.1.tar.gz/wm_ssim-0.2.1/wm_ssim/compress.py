import os
import sys
from PIL import Image
import numpy
import magic
import shutil


#compresses by taking image quality
def compress_image(src_folder,target_folder,img_file,new_name,quality_metric):
	ext_dict = {"jpg":"JPEG","jpeg":"JPEG","png":"PNG","gif":"GIF"}
	file_info = magic.from_file(src_folder+'/'+img_file, mime=True)
	img_ext = file_info.split('/')[-1]

	#check if image format is recognized
	if img_ext not in ext_dict.keys():
		#print "Error: unrecognized image extension {} in file {}".format(img_ext,src_folder+'/'+img_file)
		return -1,-1,-1
	format = ext_dict[img_ext]

	#limiting image quality between 1 and 100. can be changes
	if not(1 <= quality_metric <= 100):
		print ("Error: Quality must be in the range {} to {}. Given value: {}".format(1,100,quality_metric))
		sys.exit(1)
	filepath = os.path.join(os.getcwd(), src_folder+"/"+img_file)
	oldsize = float(os.stat(filepath).st_size/1000.0)
	picture = Image.open(filepath)
	newpath = os.path.join(os.getcwd(),target_folder+"/"+new_name)
	picture.save(target_folder+"/"+new_name,format,optimize=True,quality=quality_metric) 
	newsize = float(os.stat(newpath).st_size/1000.0)
	percent = (oldsize-newsize)/float(oldsize)*100
	return oldsize,newsize,percent


#tells which value is in the 1 to 100 range
def val_in_range(low,high):
	val_range = range(1,101)
	
	if (high in val_range) and (low in val_range):
		return (low+high)/2
	elif high in val_range:
		return high
	elif low in val_range:
		return low
	else:
		print ("Error in val_in_range: low value {} and high value {} both out of range".format(low,high))
		sys.exit(1)

def size_comparison(newsize,org_size,percentage):
	slack = 1 #percent
	percent_upper = percentage+slack
	percent_lower = percentage-slack
	percent_achieved = (1 - (float(newsize)/float(org_size)))*100

	if percent_achieved<percent_lower: #not enough size reduction achieved
		return  1
	elif percent_achieved>percent_upper: #too much reduction achieved
		return -1
	else:
		return 0

def quality_binary_search(filepath,percentage,low,high,org_size,format,ext):
	#no ideal quality found. Returns either high or low(whichever is in the 1-100 range)
	if high<low:
		return val_in_range(low,high)

	mid = int((low+high)/2)
	new_filename = "size_test."+ext
	picture = Image.open(filepath)
	picture.save(new_filename,format,optimize=True,quality=mid)
	newsize = float(os.stat(new_filename).st_size/1000.0)
	#checking image size
	size_comp = size_comparison(newsize,org_size,percentage)
	#delete photo after checking size
	os.remove(new_filename)
	if size_comp==0: #size in range
		return mid
	elif size_comp==-1: #size too low
		return quality_binary_search(filepath,percentage,mid+1,high,org_size,format,ext)
	elif size_comp==1: #size too high
		return quality_binary_search(filepath,percentage,low,mid-1,org_size,format,ext)


#compresses by taking percentage reduction
def compress_image_by_percentage(src_folder,target_folder,img_file,new_name,percentage_reduction):
	ext_dict = {"jpg":"JPEG","jpeg":"JPEG","png":"PNG","gif":"GIF"}
	file_info = magic.from_file(src_folder+'/'+img_file, mime=True)
	img_ext = file_info.split('/')[-1]

	#check if image format is recognized
	if img_ext not in ext_dict.keys():
		print ("Error: unrecognized image extension {} in file {}".format(img_ext,src_folder+'/'+img_file))
		return -1,-1,-1,-1
	format = ext_dict[img_ext]

	#limiting percentage reduction between 0 and 100%. Can be extended
	if not(0 <= percentage_reduction <= 100):
		print ("Error: Percentage must be in the range {} to {}".format(0,100))
		sys.exit(1)

	filepath = os.path.join(os.getcwd(), src_folder+"/"+img_file)
	oldsize = float(os.stat(filepath).st_size/1000.0)

	#finding quality level to achieve desired percentage reduction
	quality_level = quality_binary_search(filepath,percentage_reduction,1,100,oldsize,format,img_ext)

	picture = Image.open(filepath)
	newpath = os.path.join(os.getcwd(),target_folder+"/"+new_name)
	picture.save(target_folder+"/"+new_name,format,optimize=True,quality=quality_level) 
	newsize = float(os.stat(newpath).st_size/1000.0)
	percent = (oldsize-newsize)/float(oldsize)*100

	#handle case in which compression increased image size
	if percent<0:
		os.remove(newpath)
		shutil.copyfile(filepath,newpath)
		return oldsize,oldsize,0,-1		

	return oldsize,newsize,percent,quality_level


if __name__=='__main__':
	src_folder = sys.argv[1]
	percentage_reduction = 25
	target_folder = src_folder+"_compressed_"+str(percentage_reduction)
	if not os.path.isdir(target_folder):
		os.mkdir(target_folder)
	images = os.listdir(src_folder)
	percentages = []
	for img in images:
		oldsize,newsize,percent,quality = compress_image_by_percentage(src_folder,target_folder,img,"Compressed_"+img,percentage_reduction)
		#percentages.append(percent)
		#print "Image {} compressed by {} percent from {} KB to {} KB ::: Quality Metric : {}".format(img,percent,oldsize,newsize,quality_metric)
		print ("Img {} -> Target Percentage: {} Percentage Achieved: {} Quality: {}".format(img,percentage_reduction,percent,quality))
	# avg = sum(percentages)/len(percentages)
	# print "Average compression for quality {} is {} percent".format(quality_metric,avg)
	# print "Standard deviation for quality {} is {} percent".format(quality_metric,numpy.std(percentages))

