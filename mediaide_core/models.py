from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser

# Create your models here.
from mediaide_core.manager import UserManager
from django.utils.translation import ugettext_lazy as _

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_of_birth = models.DateTimeField(_('date of birth'), auto_now_add=True)
    phone = models.IntegerField(null=True,blank=True)
    gender = models.CharField( max_length=1, choices=GENDER_CHOICES)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=True)
    term_and_condition = models.BooleanField(_('T&C'), default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Address(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    address1 = models.CharField("Address line 1", max_length=1024)
    address2 = models.CharField("Address line 2", max_length=1024)
    zip_code = models.CharField("ZIP / Postal code", max_length=12)
    city = models.CharField("City", max_length=1024)
    0#TODO we have to give iso country name list as chooise
    country = models.CharField("Country", max_length=3,
                               )


class TermsAndConditions(models.Model):
    description = models.TextField()


class UserDocuments(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='document')
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class CountryVisa(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=75)
    phone = models.IntegerField()
    fax = models.CharField(max_length=20)
    website = models.URLField(max_length=200, null=True, blank=True)
    embassy = models.CharField(max_length=255)

    def __unicode__(self):
        return "{}-{}".format(self.name,self.embassy)


class MedicalPackages(models.Model):
    name_of_treatment  =  models.CharField(max_length=255)
    no_of_days_in_hospital = models.IntegerField(default=1)
    no_of_days_out_hospital = models.IntegerField(default=0)
    approximate_cost = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name_of_treatment


class UserTreatmentPackages(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    treatment_package = models.ForeignKey(MedicalPackages,on_delete=models.CASCADE)

    def __unicode__(self):
        return "{}-{}".format(self.user,self.treatment_package)


class UserEnquiry(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateTimeField(auto_now_add=True)
    phone = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(_('email address'), unique=True)
    message =models.TextField(null=True, blank=True)
    appointment_date =  models.DateTimeField(_('appointment date'), auto_now_add=True)
    #TODO we have to make list
    reason = models.CharField(max_length=255)

    def __unicode__(self):
        return "{}-{}".format(self.name, self.appointment_date)


class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(_('email address'), unique=True)
    message = models.TextField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Facilities(models.Model):
    name = models.CharField(max_length=255)
    cost = models.IntegerField()

    def __unicode__(self):
        return "{}-{}".format(self.name, self.cost)
