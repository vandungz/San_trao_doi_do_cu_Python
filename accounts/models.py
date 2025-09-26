from django.db import models
from django.contrib.auth.models import User
import pyotp
import base64
import os
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=32, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.otp_secret:  # chỉ tạo secret lần đầu
            self.otp_secret = base64.b32encode(os.urandom(10)).decode("utf-8")
        super().save(*args, **kwargs)

    def get_totp_uri(self):
        return f"otpauth://totp/SanTraoDoiDoCu:{self.user.username}?secret={self.otp_secret}&issuer=SanTraoDoiDoCu"

    def verify_token(self, token):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(token)

    def __str__(self):
        return f"Profile of {self.user.username}"

#Signal: tự động tạo UserProfile khi User mới được tạo
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


