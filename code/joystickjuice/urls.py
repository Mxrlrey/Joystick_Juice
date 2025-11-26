from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('acesso/', include("django.contrib.auth.urls")),
    path("", include("user.urls")),
    path("", include("game.urls")),
    path('review/', include('review.urls')),
]
