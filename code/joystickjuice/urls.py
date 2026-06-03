from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

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
    path('client/', TemplateView.as_view(template_name='api_client/login.html'), name='api_client_login'),
    path('client/games/', TemplateView.as_view(template_name='api_client/games.html'), name='api_client_games'),
    path('client/games/form/', TemplateView.as_view(template_name='api_client/game_form.html'), name='api_client_game_form'),
    path('', include('game.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
