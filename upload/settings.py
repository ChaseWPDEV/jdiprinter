"""
	This file controls the Settings form and the logo upload form in the Dicom label app
"""

from django import forms
from .models import SettingsField, ImageLogo
import os

class SettingsForm(forms.Form):
	#dictionary with dicom file attributes:readable label

	dicom_fields={'PatientName':'Patient Name',
			'ProtocolName':'Protocol/Contrast',
			'ReferringPhysiciansName':'Physician',
			'RequestedProcedureDescription':'Procedure Descritpion',
			'StudyDate': 'Study date',
			'StudyID': 'Study ID',
			'PatientID': 'Patient ID',
			'AccessionNumber': 'Accession #',
			'InstitutionName': 'Institution Name',
			'StudyDescription': 'Study Desc.'
			}
	
	def __init__(self, *args, **kwargs):
		super(SettingsForm, self).__init__(*args, **kwargs)

		#routine to verify each dictionary setting is in the model
		setting_keys=SettingsField.objects.all().values_list('setting_key', flat=True)
		for k in SettingsForm.dicom_fields:
			
			if k in setting_keys:
				continue

			s=SettingsField(setting_key=k, enabled=False)
			s.save()

		settings=SettingsField.objects.all()

		#set form fields to match current entry in the model		
		for stg in settings:
			self.fields[stg.setting_key]=forms.BooleanField(initial=stg.enabled,
					label=SettingsForm.dicom_fields[stg.setting_key], 
					required=False)
		self.fields['delete']=forms.BooleanField(initial=False, label="Delete Logo", required=False)

	#Custom save method
	def save(self):
		data=self.cleaned_data
		
		for k in SettingsForm.dicom_fields:
			s=SettingsField(setting_key=k)
			if data[k]:
				s.enabled=True
			else:
				s.enabled=False
			s.save()
		
		if data['delete']:
			try:
				il=ImageLogo.objects.get(zero=0)
				os.remove(il.image.path)
				il.delete()
			finally:
				return
		

class LogoForm(forms.Form):
	logo=forms.FileField(required=False)

	#custom save method with hard coded "logo" name
	def save(self, f):
		ext=os.path.splitext(f.name)[1]
		name='logo'+ext

		with open('/var/www/html/media/'+name, 'wb+') as destination:
			for chunk in f.chunks():
				destination.write(chunk)
		il=ImageLogo(zero=0)
		il.image.name=name
		il.save()
	



