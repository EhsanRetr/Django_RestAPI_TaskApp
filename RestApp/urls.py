from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from users import router as user_api_router
from home import router as house_api_router
from django.conf.urls.static import static
from Task import router as task_api_router




auth_api_urls = [
    path(r'',include('drf_social_oauth2.urls',namespace='drf_social_oauth2')),
]
if settings.DEBUG:
    auth_api_urls.append(path(r"verify/",include('rest_framework.urls')))

api_url_pattern = [
    path("auth/",include(auth_api_urls)),
    path(r"accounts/",include(user_api_router.router.urls)),
    path(r"house/",include(house_api_router.router.urls)),
    path(r'task/',include(task_api_router.router.urls))
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/",include(api_url_pattern)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)