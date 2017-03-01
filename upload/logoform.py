
from .models import SettingsField, ImageLogo
from .dchandler import LabelFactory
from . import labeldata as label

from PIL import Image
from django import forms

class LogoForm(forms.Form):
	logo=forms.FileField(required=False)
	aspect=label.width/label.height
	resize_method=Image.LANCZOS
	

	def save(self,f):
		logo=Image.open(f)
		
		#resize routine
		if logo.size[0]<label.width and logo.size[1]<label.height:
			logo_aspect=logo.size[0]/logo.size[1]
			if logo_aspect>=self.aspect:
				#resize to width
				new_height=int(label.width/logo_aspect)
				new_size=(label.width, new_height)
			else:
				#resize to height
				new_width=int(label.height*logo_aspect)
				new_size=(new_width, label.height)
			logo=logo.resize(new_size, resample=self.resize_method)

		im=Image.new("L",(label.width,label.height),"white")
		logosize=label.width, label.height
		logo.thumbnail(logosize, Image.ANTIALIAS)
		logox=int(label.width/2)-int(logo.size[1]/2)
		im.paste(logo,(logox,0))
		fullpath=label.filepath+label.name
		im.save(fullpath)

		il=ImageLogo(zero=0)
		il.image.name=label.name
		il.save()

	#custom save method with hard coded "logo" name
	def old_save(self, f):
		ext=os.path.splitext(f.name)[1]
		name='logo'+ext

		with open('/var/www/html/media/'+name, 'wb+') as destination:
			for chunk in f.chunks():
				destination.write(chunk)
		il=ImageLogo(zero=0)
		il.image.name=name
		il.save()
