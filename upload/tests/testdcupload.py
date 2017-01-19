from django.test import TestCase, RequestFactory
from upload.views import index, settings,get_fields, print_label
from upload.settings import SettingsForm
from ..dchandler import process_upload, LabelFactory
from ..models import SettingsField
from django.core.files.uploadedfile import SimpleUploadedFile
import os

import upload.globs as globs
import pydicom


class UploadTestCase(TestCase):
	def setUp(self):
		self.factory=RequestFactory()
	
	def test_upload_template(self):
		request=self.factory.get('/')
		with self.assertTemplateUsed('index.html'):
			response=index(request)
		self.assertEqual(response.status_code, 200)

	def test_process_upload(self):
		for k in SettingsForm.dicom_fields:
			s=SettingsField(setting_key=k, enabled=True)
			s.save()
		tfields=SettingsField.objects.all().filter(enabled=True)
		self.assertEqual(len(SettingsForm.dicom_fields), len(tfields))

		content_type = "multipart/form-data; boundary=------------------------1493314174182091246926147632"
		request=self.factory.post('/', content_type=content_type)
		test_file=SimpleUploadedFile(name="sample.dcm", content=open("upload/tests/sample.dcm",'rb').read())
		request.FILES.update({"file":test_file})

		process_upload(request.FILES['file'])
		self.assertFalse(os.path.isfile('media/output.png'))
		self.assertFalse(os.path.isfile('media/output.bin'))

	def test_jdidicom_request(self):
		for k in SettingsForm.dicom_fields:
			s=SettingsField(setting_key=k, enabled=True)
			s.save()

		request=self.factory.get(globs.active_fields)
		resp=get_fields(request)
		fields=eval(str(resp.content,'utf-8'))
		
		self.assertTrue(isinstance(fields, dict))
		
		dc=pydicom.read_file("upload/tests/sample.dcm")
		print_url=globs.print_label
		params={}
		
		for k in fields:			
				f=str(getattr(dc, k))
				params[k]=f
		self.assertEqual(len(SettingsForm.dicom_fields), len(params))

		request=self.factory.get(print_url, data=params)
		print_label(request)
		lf=LabelFactory()
		lines=lf.make_label_from_dict(params)
		self.assertEqual(len(SettingsForm.dicom_fields), lines)
		
