## playlist-tools-server/tools/urls.py


from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('api/', include('tools.api.urls'))
]
