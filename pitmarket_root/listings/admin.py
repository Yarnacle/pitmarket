from django.contrib import admin
from .models import Listing

class ListingAdmin(admin.ModelAdmin):
	list_display = ['id','item','price','username','tag_list','list_date']
	list_filter = ['list_date']
	ordering = ['-list_date']
	search_fields = ['id','list_date']

	def get_queryset(self,request):
		return super().get_queryset(request).prefetch_related('tags')

	def tag_list(self,obj):
		return u', '.join(o.name for o in obj.tags.all())

admin.site.register(Listing,ListingAdmin)