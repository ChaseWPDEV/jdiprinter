from django.conf.urls import url

from . import views
from . import globs

urlpatterns=[
    url(r'^$', views.settings, name='settings'),
	url(r'logo/', views.logo, name='logo'),
    url(r'settings/', views.settings, name='settings'),
	url(globs.print_label, views.print_label, name='print_label'),
	url(globs.active_fields, views.get_fields, name='get_fields'),
]
