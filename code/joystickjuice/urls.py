from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('access/', include('django.contrib.auth.urls')),
    path('account/', include('user.urls')),
    path('game/', include('game.urls')),
    path('review/', include('review.urls')),
    path('club/', include('club.urls')),
    path('collections/', include('collection.urls')),
    path('api/', include('api.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', include('game.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
