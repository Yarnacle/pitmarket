from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.site.site_header = 'Pit Market administration'
admin.site.site_title = 'Pit Market site admin'

urlpatterns = [
   path('admin/',admin.site.urls),
	path('admin/defender/',include('defender.urls')),
	path('',include('listings.urls')),
	path('',include('pages.urls'))
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)