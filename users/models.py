from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICE = (
    ('M','Male'),
    ('F','Female'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=6, choices = GENDER_CHOICE)
    image = models.ImageField(upload_to='profile', default='https://thumbs.dreamstime.com/b/user-profile-icon-vector-avatar-person-picture-portrait-symbol-neutral-gender-silhouette-circle-button-photo-blank-272664038.jpg')
    # created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.full_name
