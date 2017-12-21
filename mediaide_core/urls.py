from django.conf.urls import  url,include

from mediaide_core import views
from mediaide_core.views import Logout, ResendMes, UserEnquiryView, CustomUserView, MedicalPackagesView, \
    CountryVisaView, FacilitiesView, ContactUsView, user_login, get_estimate_data
from .views import RegisterUser

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'get-user', CustomUserView)
router.register(r'medical-package', MedicalPackagesView)
router.register(r'country-visa', CountryVisaView)
router.register(r'facilities', FacilitiesView)
router.register(r'user-enquiry', UserEnquiryView)
router.register(r'contact-us', ContactUsView)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register/$', RegisterUser.as_view()),
    url(r'^logout/$', Logout.as_view()),
    url(r'^login/$', user_login),
    url(r'^get-estimate/$', get_estimate_data),
    url(r'^resend-confirmation-mail/$', ResendMes.as_view()),
    url(r'^confirm/(?P<confirmation_code>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<username>[\w]+)/$',
        views.confirm,name='confirm'),
]