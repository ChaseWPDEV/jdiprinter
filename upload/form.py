""" The core upload form of the Dicom label printer
"""

from django import forms

class DCPUploadFileForm(forms.Form):
	file=forms.FileField()
