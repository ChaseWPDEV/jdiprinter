"""
	Methods for index, settings and logo views
	Links display templates to save logic
"""

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import loader
from django.core.files import File
from django.urls import reverse

from .form import DCPUploadFileForm
from .dchandler import process_upload, get_active_fields, LabelFactory

from .settings import SettingsForm, LogoForm
from .models import ImageLogo

import random
import urllib.parse

# index method displays core upload form and forwards dicom uploads to handler for processing
def index(request):
	if request.method == 'POST':
		form=DCPUploadFileForm(request.POST, request.FILES)
		#process upload if file has been posted
		if form.is_valid():
			process_upload(request.FILES['file'])			
	else:
		form=DCPUploadFileForm()
	return render(request, 'index.html', {'form': form})

#settings allows user to select fields to render on the label and displays logo
def settings(request):
	form=SettingsForm(request.POST or None, request.FILES or None)
	
	if request.method=='POST':
		if form.is_valid():
			form.save()
	try:
		logo=ImageLogo.objects.get(zero=0)
	except:
		logo={}
	widgets={'logo':logo, 'form':form, 'rand':random.randrange(10000)}
	return render(request, 'settings.html', widgets)

#logo allows user to upload logo for dispaly on label
def logo(request):
	form=LogoForm(request.POST or None, request.FILES or None)
	
	if request.method=='POST':
		if form.is_valid():
			form.save(request.FILES['logo'])
			return (HttpResponseRedirect('/settings/'))
	
	return render(request, 'logo.html', {'form': form})

def print_label(request):
	#Guard Statements
	if request.method!='GET':
		return
		
	#Print Logo
	LF=LabelFactory()
	LF.make_logo_label()

	
	#Parse Get Values
	values={}
	for k in SettingsForm.dicom_fields:
		values[k]=request.GET.get(k, False)
	
	#Print label
	LF.make_label_from_dict(values)
	return HttpResponse(' ');

def get_fields(request):
	fields=get_active_fields();
	return HttpResponse(str(fields))

