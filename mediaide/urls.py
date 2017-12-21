from django.conf.urls import include, url
from rest_framework_jwt.views import obtain_jwt_token

from django.contrib import admin

from mediaide_core.views import CustomUserView

admin.autodiscover()

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^login/', obtain_jwt_token),
    url(r'^api/', include('mediaide_core.urls')),

    # ... your url patterns
]
