from django.test import TestCase, RequestFactory

import upload.globs as globs
import upload.dchandler as dch
from upload.views import get_fields

from upload.settings import SettingsForm
from upload.models import SettingsField


class GetFieldsTestCase(TestCase):

	def setUp(self):
		self.factory=RequestFactory()
		request=self.factory.get('/'+globs.active_fields)
		self.response=get_fields(request)

	def test_url(self):
		self.assertEqual(self.response.status_code, 200)

	def test_fields(self):
		for k in SettingsForm.dicom_fields:
			s=SettingsField(setting_key=k, enabled=True)
			s.save()
		fields=dch.get_active_fields()
		request=self.factory.get('/'+globs.active_fields)
		self.response=get_fields(request)
		self.assertEqual(len(SettingsForm.dicom_fields), len(fields))
		self.assertEqual(str(self.response.content, 'utf-8'), str(fields))

		
