import glob
import shutil
import os
from PIL import Image
import glob,os
def movefiles():
	#parent_dir = r"C:\\Users\\Madhu\\Documents\\Final_Year_Project\\Project_Code\\BreaKHis_v1_Aug\\histology_slides\\breast\\malignant\\SOB\\ductal_carcinoma"
	src_dir = "C:\\Users\\Madhu\\Documents\\Final_Year_Project\\Project_Code\\BreaKHis_v1_Aug\\histology_slides\\breast\\malignant\\SOB\\papillary_carcinoma\\"
	dst_dir = "C:\\Users\\Madhu\\Documents\\Final_Year_Project\\Project_Code\\BreaKHis_v1_Aug\\histology_slides\\breast\\malignant\\SOB\\400X\\papillary_carcinoma\\"
	for filename in glob.iglob(src_dir + '*\\400X\\*.png', recursive=True):
		print("Moving")
		shutil.move(filename,dst_dir)
	#remove existing folders
	for dir in glob.iglob(src_dir+'*\\400X',recursive=True):
		shutil.rmtree(dir)
		print("removed")

def tojpg():
	folder=r'C:\Users\Madhu\Documents\Final_Year_Project\Project_Code\BreaKHis_v1_Aug\histology_slides\breast\malignant\SOB\400X\papillary_carcinoma\*.png'
	imList=glob.glob(folder)
	# Loop through all the image:
	for img in imList:
		#extract the filename and extension from path 
		fileName,fileExt = os.path.splitext(img)
		#open the image
		im = Image.open(img)
		if(im):
			rgb_im = im.convert("RGB")
			rgb_im.save(fileName+'.jpg') 
			print("DONE")
		else:
			os.remove(img)
			print("Cannot convert removing")
	# save the image in the same folder, with the same name, except *.png

movefiles()
tojpg()


   