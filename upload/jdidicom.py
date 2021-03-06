

from pynetdicom3 import AE, StorageSOPClassList, VerificationSOPClass
import pydicom as pdc
from pydicom.dataset import Dataset, FileDataset
import requests
from importlib.machinery import SourceFileLoader
import upload.globs as glob
import os
import time

class JDIAE(AE):
	url_base='http://localhost/'

	def __init__(self, *args, **kwargs):
		kwargs['scp_sop_class']=[VerificationSOPClass]+StorageSOPClassList
		super(JDIAE, self).__init__(*args, **kwargs)
		self.maximum_associations = 5
		self.network_timeout=0
		self.last_pt=None
		self.last_time=0

	def _cleanup_associations(self):
		start=len(self.active_associations)
		super(JDIAE, self)._cleanup_associations()
		if len(self.active_associations)==0:
			self.last_pt=None
			if start>0:
				self.last_time=time.time()

	def on_c_store(self, dataset):
		success=0x0000
		if self.last_pt is not None:
			return success
		
		delay=time.time()-self.last_time
		if delay<5:
			return success

		ds=FileDataset('/tmp/1.dcm',dataset)
		ds.save_as('/tmp/1.dcm')
		dc=pdc.read_file('/tmp/1.dcm', force=True)
		os.remove('/tmp/1.dcm')

		if dc.PatientName==self.last_pt:
			return success
		else:
			self.last_pt=dc.PatientName
			s=requests.session()
			resp=s.get(self.url_base+glob.active_fields)
			fields=eval(str(resp.content,'utf-8'))

			if not isinstance(fields, dict):
				raise Exception('Bad dictionary passed')
			
			print_url=self.url_base+glob.print_label+'?'
			for k in fields:
				try:			
				    print_url+=k+'='+str(getattr(dc, k))+'&'
				except:
				    pass
			s.get(print_url)

			return success
