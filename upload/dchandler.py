"""
Create image from dicom image upload, based on settings and logo
"""
import os
from django.core.exceptions import ValidationError
from .models import SettingsField, ImageLogo
from .settings import SettingsForm
import pydicom as dicom

from .labeldata import LabelData

from PIL import Image, ImageFont, ImageDraw

class LabelFactory():
	#width=696
	#height=306
	#fontsize=50
	#whitespace=10
	#filepath="/var/www/html/media/"
	filename="output.png"
	binname="output.bin"
	no_print=['Patient Name', 'Institution Name']
	mode="L"

	def make_logo_label(self):
		if ImageLogo.objects.filter(zero=0).count()==0:
			return
		
		fullpath=LabelData.filepath+LabelData.name
		self.print_label(fullpath)

	def make_label_from_dict(self, d):
		font=ImageFont.truetype(LabelData.filepath+"LibSerif.ttf", LabelData.fontsize)
		fields=SettingsField.objects.all()
		labels=SettingsForm.dicom_fields
		text=[]
		for f in fields:
			if f.enabled and (f.setting_key in d) and d[f.setting_key]:
				label=labels[f.setting_key]
				text+=[[label,d[f.setting_key].replace('^',' ')]]
	
		im=Image.new(self.mode,(LabelData.width,LabelData.height),"white")
		i=0
		draw=ImageDraw.Draw(im)
		for k in text:
			line=''
			if k[0] not in self.no_print:
				line+=k[0]+':'
			line+=k[1]
			draw.text((0,i),line,"black",font=font)
			i+=LabelData.fontsize
	
		fullpath=LabelData.filepath+self.filename
		im.save(fullpath)
		self.print_label(fullpath)
		return len(text)
		
		
	def print_label(self, filename):
		model="QL-700"
		label_size="62"
		rotate="0"
		bin_file=LabelData.filepath+self.binname
		command="brother_ql_create"
		command+=" --model "+model
		command+=" --label-size "+label_size
		#command+=" --rotate "+rotate
		command+=" "+filename+" > "+bin_file
		os.system(command)
		dev="/dev/usb/lp0"
		print_com="cat "+bin_file+" > "+dev
		os.system(print_com)
		os.remove(filename)
		os.remove(bin_file)
		

def get_active_fields():
	fields=SettingsField.objects.all().filter(enabled=True)
	output={}
	labels=SettingsForm.dicom_fields
	for f in fields:
		output[f.setting_key]=labels[f.setting_key]

	return output




#Processes dicom image to produce output.png(hardcoded)
#Hardcode sizing (based on label), font size, and output.png
#Produces black/white image 
def process_upload(f):
	validate_file_extension(f)
	lf=LabelFactory()
	lf.make_logo_label()
	lf.make_text_label(f)
	return True

#Basic validation as dicom file
def validate_file_extension(value):
	ext=os.path.splitext(value.name)[1]
	valid_extensions=['.dcm']
	if not ext.lower() in valid_extensions:
		raise ValidationError(u'Not a Dicom file.')



