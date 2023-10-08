
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = "The Watch Gallery"
admin.site.site_title = "Kumar Admin"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('froala_editor/',include('froala_editor.urls')),
    path('',include('watch.urls')),
    path('watchauth/',include('watchauth.urls')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('', include('repair_app.urls')),
    path('summernote/', include('django_summernote.urls')),


    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
