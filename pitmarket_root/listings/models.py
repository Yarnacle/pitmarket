from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from .validators import validate_file_size

class Listing(models.Model):
	item = models.CharField(max_length = 100)
	price = models.CharField(max_length = 100)
	description = models.TextField('Description')
	contact = models.CharField(max_length = 100)
	image = models.ImageField(upload_to='uploads/',blank = True,validators = [validate_file_size])
	list_date = models.DateTimeField('List Date',auto_now_add = True)
	id = models.AutoField(primary_key = True)
	tags = TaggableManager()
	username = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id)