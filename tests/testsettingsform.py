
from django.test import TestCase, RequestFactory
from upload.views import settings
from upload.settings import SettingsForm 
from upload.models import SettingsField


class SettingsFormTestCase(TestCase):
	def setUp(self):
		self.factory=RequestFactory()
	
	def test_settings_template(self):
		request=self.factory.get('/settings/')
		with self.assertTemplateUsed('settings.html'):
			response=settings(request)
		self.assertEqual(response.status_code, 200)
	

	def test_form_atts(self):
		sf=SettingsForm()
		self.assertTrue(len(sf.fields)>0)
		self.assertEqual(len(sf.fields), len(SettingsForm.dicom_fields)+1)

	def test_form_post(self):
		post_dict={}
		for k in SettingsForm.dicom_fields:
			post_dict[k]='on'
		request=self.factory.post('/settings/', post_dict)

		sf=SettingsForm(request.POST, request.FILES)
		self.assertTrue(sf.is_valid())
		sf.save()
		data=SettingsField.objects.all()
		for obj in data:
			self.assertTrue(obj.enabled)
