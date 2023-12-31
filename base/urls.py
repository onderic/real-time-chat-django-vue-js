from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/v1/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
