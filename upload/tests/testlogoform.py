
from django.test import TestCase, RequestFactory

from upload.settings import LogoForm
from upload.models import ImageLogo
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from upload.views import logo

class LogoFormTestCase(TestCase):
	def setUp(self):
		self.filepath='/home/chasegru/localdj/dcprinter/media/smallacorn.png'
		self.filename='smallacorn.png'
		self.factory=RequestFactory()
	
	def test_upload_template(self):
		request=self.factory.get('/logo/')
		with self.assertTemplateUsed('logo.html'):
			response=logo(request)
		self.assertEqual(response.status_code, 200)
	
	def test_logo_form_logic(self):
		f=open(self.filepath, 'rb').read()
		test_file=File(f)
		il=ImageLogo(zero=0)
		il.image.name=self.filename
		il.save()

		self.assertTrue(il.image.path==self.filepath)

	def test_logo_form(self):
		content_type = "multipart/form-data; boundary=------------------------1493314174182091246926147632"
		request=self.factory.post('/settings/', content_type=content_type)
		test_file=SimpleUploadedFile(name=self.filename, content=open(self.filepath,'rb').read(), content_type='image/png' )
		request.FILES.update({"logo":test_file})
		lf=LogoForm(request.POST, request.FILES)
		
		self.assertTrue(lf.is_valid())
		lf.save(request.FILES['logo'])
		
		il=ImageLogo.objects.get(zero=0)
		self.assertTrue('logo.png' in il.image.path)
