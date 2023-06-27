from django.db import models

class BlogPost(models.Model):
	title = models.CharField(max_length = 100,unique = True)
	content = models.TextField('Page Content')
	upload_date = models.DateTimeField('Publish Date',auto_now_add = True)

	def __str__(self):
		return self.title