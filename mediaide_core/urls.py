from django.conf.urls import  url

from mediaide_core import views
from mediaide_core.views import Logout, ResendMes
from .views import RegisterUser

urlpatterns = [
    url(r'^register/$', RegisterUser.as_view()),
    url(r'^logout/$', Logout.as_view()),
    url(r'^resend-confirmation-mail/$', ResendMes.as_view()),
    url(r'^confirm/(?P<confirmation_code>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<username>[\w]+)/$',
        views.confirm,name='confirm'),
    # url(r'^resend-confirmation-mail/$',
    #     views.resend_confirmation_code,name='resend_confirmation_code'),
]