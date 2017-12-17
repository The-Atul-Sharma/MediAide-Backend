from django.contrib import admin

from mediaide_core.models import MedicalPackages, CustomUser, UserTreatmentPackages, TermsAndConditions, Address, \
    UserEnquiry, Facilities, ContactUs, UserDocuments,CountryVisa
# Register your models here.

admin.site.register(CountryVisa)
admin.site.register(MedicalPackages)
admin.site.register(CustomUser)
admin.site.register(UserTreatmentPackages)
admin.site.register(TermsAndConditions)
admin.site.register(Address)
admin.site.register(UserEnquiry)
admin.site.register(Facilities)
admin.site.register(ContactUs)
admin.site.register(UserDocuments)
