from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from gdstorage.storage import GoogleDriveStorage
from config import settings
from plants_api.helpers import helpers
from django.db.models.signals import pre_save

# Create your models here.

gd_storage = GoogleDriveStorage()

class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    temporal_password  = models.CharField(_("Temporal Password"), blank=True , null=True, max_length=255)
    email = models.EmailField(unique=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

class Profile(models.Model):
    number_id = models.PositiveIntegerField("Número de referencia" , unique = True)
    phone =  models.CharField(max_length=100 , verbose_name="Teléfono")
    photo = models.ImageField("foto de perfil" , null = True , blank = True , upload_to = "uploads/perfiles" , storage=gd_storage, default =  settings.base.STATIC_ROOT  + "/img/user-placeholder.png")
    user = models.OneToOneField(User, on_delete=models.CASCADE , null = True , blank = True)
    photo_url = models.CharField(max_length=100 , verbose_name="Url de imagen" , null = True , blank = True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "perfiles"

    def __str__(self):
        return "%s" % (self.number_id)

pre_save.connect(helpers.save_image_url, sender=Profile)
