from django.db import models

# Basic model to handle label settings
class SettingsField(models.Model):
	setting_key=models.CharField(max_length=70, primary_key=True)
	enabled=models.BooleanField()

# Dummy model to handle lable logo
class ImageLogo(models.Model):
	zero=models.SmallIntegerField(primary_key=True)
	image=models.ImageField()
