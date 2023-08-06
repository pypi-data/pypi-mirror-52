import os
import sys
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit
import shutil
import re
import copy

def get_files_in_folder(folder_path):
	files = []
	contents = os.listdir(folder_path)
	for item in contents:
		item_path = folder_path + '/' + item
		if os.path.isfile(item_path):
			files.append(item)

	return files

def filename_no_ext(file_name):
	name_list = file_name.split('.')[:-1]

	fnl_name = ""
	rep = 0
	for item in name_list:
		if rep>0:
			fnl_name += '.'
		fnl_name += item
		rep +=1

	return fnl_name

def file_ext_from_name(file_name):
	return file_name.split('.')[-1]

def filepath_for_browser(path):
	abs_path = "file://" + os.getcwd() + '/' + path
	return abs_path

def page_pretty(page_path):
    reload(sys)
    sys.setdefaultencoding('utf8')

    with open(page_path, "rb") as f:
        html_string = f.read()
        html_string = BeautifulSoup(html_string, 'html.parser').prettify()
    
    with open(page_path, "wb") as f:
        html_string.encode('ascii', 'ignore').decode('ascii')
        f.write(html_string)

def default_folders_arrangement(filepath,file_name,folder_suffix):
    main_folder_path = "".join(filepath.split("/")[:-1])
    folder_name = main_folder_path + '/' + file_name + folder_suffix
    
    if not os.path.exists(folder_name):
        return
    else:
        contents = os.listdir(folder_name)
        for item in contents:
            if os.path.isfile(folder_name+'/'+item):
                os.remove(folder_name+'/'+item)
        ####### relocating files folder ##########
        for item in os.listdir(folder_name):
            shutil.move(folder_name+'/'+item,main_folder_path+'/'+item)

def plot_graph(xvals,yvals,title,xlabel,ylabel,figname,dest_dir_path):
	fig_path = dest_dir_path+'/'+figname
	plt.plot(xvals,yvals)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.savefig(fname=fig_path)
	plt.clf()

def plot_mult_lines(xvals,yvals,colors,markers,labels,title,xlabel,ylabel,figname,dest_dir_path):
	fig_path = dest_dir_path+'/'+figname

	for x,y,c,m,l in zip(xvals,yvals,colors,markers,labels):
		plt.plot(x,y,color=c,marker=m,label=l)

	plt.legend()
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.savefig(fname=fig_path)
	plt.clf()

def plot_bar_chart(xvals,yvals,title,xlabel,ylabel,figname,dest_dir_path):
	fig_path = dest_dir_path+'/'+figname
	y_pos = np.arange(len(xvals))
	plt.bar(x=y_pos, height=yvals)
	plt.gca().yaxis.grid(True)
	plt.xticks(y_pos,xvals)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.savefig(fname=fig_path)
	plt.clf()

def line_of_best_fit(xvals,yvals,title,xlabel,ylabel,figname,dest_dir_path):
	b, m = polyfit(xvals, yvals, 1)
	plt.plot(xvals, yvals, '.')
	yvals_bf = b + m * np.array(xvals)
	plt.plot(xvals, yvals_bf, '-',label='y = {} * x + {}'.format(m,b))
	plt.legend()

	fig_path = dest_dir_path+'/'+figname
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.savefig(fname=fig_path)
	plt.clf()

def plot_cdf(plot_data_list,title,xlabel,ylabel,figname,dest_dir_path,stats_file):
	f = open(stats_file,"w+")
	for item in plot_data_list:
		sorted_points = np.sort(item['datapoints'])
		y_points = 1. * np.arange(len(sorted_points))/(len(sorted_points))
		plt.plot(sorted_points,y_points,color=item['color'],label=item['label'])
		f.write("{} -> LowerQuart: {} Median: {} UpperQuart: {}\n".format(item['label'],np.percentile(item['datapoints'], 25),np.percentile(item['datapoints'], 50),np.percentile(item['datapoints'], 75)))
	plt.legend()
	f.close()

	fig_path = dest_dir_path+'/'+figname
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.savefig(fname=fig_path)
	plt.clf()

def sort_nicely(in_list):
	""" Sort the given list in the way that humans expect.
	"""
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
	in_list.sort(key=alphanum_key)