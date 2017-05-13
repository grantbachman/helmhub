from django.db.models.fields.files import FileField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Chart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()




class ChartVersion(models.Model):
    chart = models.ForeignKey(Chart, related_name='versions', on_delete=models.CASCADE)
    version = models.CharField(max_length=14, blank=False, null=False)
    tgz = FileField(upload_to='charts')

    class Meta:
        ordering = ['-version']

    def __unicode__(self):
        return self.version


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
