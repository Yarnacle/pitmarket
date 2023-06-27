from django.contrib import admin
from .models import BlogPost

class PostAdmin(admin.ModelAdmin):
	list_display = ['title','upload_date']
	ordering = ['-upload_date']
	search_fields = ['title','upload_date']
	readonly_fields = ['upload_date']

admin.site.register(BlogPost,PostAdmin)