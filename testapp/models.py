from django.db import models
from django import utils
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid,datetime
from django.utils.crypto import get_random_string
from django.conf import settings
from django.utils import timezone
import jwt


class CUser(models.Model):
    name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True,blank=True)
    password = models.CharField(max_length=10,null=True,blank=True)
    password_token = models.CharField(max_length=2000,editable=False)

    @property
    def password_token(self):
        time_delta = datetime.timedelta(minutes=5)
        payload = {"id": self.id,"exp": datetime.datetime.utcnow() + time_delta}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


    

class OTP(models.Model):
    '''
    For validation of OTP with expiration of each transaction
    '''
    txn_id = models.UUIDField(primary_key=True,editable=False) # for each taransaction it a uniuq id
    email_or_mobile = models.TextField(default='')             # user can provide email or mobile number
    otp = models.CharField(max_length=10)                      # OTP
    expire_at = models.DateTimeField()                         # OTP expiration time (current time + timedelta)

    class Meta:
        db_table = "otp" # Table Name

    def save(self,*args,**kwargs):
        self.txn_id = uuid.uuid4()
        self.otp  = get_random_string(4,'1234567890')
        self.expire_at = timezone.now() + datetime.timedelta(minutes=5)
        super(OTP,self).save(*args,**kwargs)

    @property
    def is_expired(self):
        exp_time = self.expire_at - timezone.now()
        if exp_time < datetime.timedelta(seconds=0):
            return True
        return False
