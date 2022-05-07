from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers

from modules.node.views import NodesViewSets, node_auth, node_list, node_last
from modules.read.views import ReadingSensorViewSets, ReadingPowerViewSets, read_sensor_post, read_power_post
from modules.user.views import staff_login, index_page, token_verify

router = routers.DefaultRouter()
router.register(r'node', NodesViewSets, basename='nodes')
router.register(r'read_sensor', ReadingSensorViewSets, basename='readings_sensor')
router.register(r'read_power', ReadingPowerViewSets, basename='readings_power')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/p/read_sensor_post/', read_sensor_post),
    path('api/p/read_power_post/', read_power_post),
    path('api/g/node_auth/', node_auth),
    path('api/g/node_list/', node_list),
    path('api/g/node_last/', node_last),
    path('api/login/', staff_login),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('login/', staff_login),
    path('token/', token_verify),
    path('', index_page)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)