import os
import uuid
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from PIL import Image


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def resize_image(sender, instance=None, update_fields=None, **kwargs):
    if not update_fields:
        return
    if "profilepic" in update_fields:
        profilepic = instance.profilepic
        fullpath = profilepic.path
        path = os.path.dirname(fullpath)
        extension = os.path.splitext(fullpath)[1]
        uid = uuid.uuid4()

        img = Image.open(fullpath).convert("RGB")
        width, height = img.size

        if width > height:
            img = img.crop(
                (
                    round((width - height) / 2),
                    0,
                    height + round((width - height) / 2),
                    height,
                )
            )
        elif height > width:
            img = img.crop(
                (
                    0,
                    round((height - width) / 2),
                    width,
                    width + round((height - width) / 2),
                )
            )

        img.save(os.path.join(path, str(uid) + ".jpg"), format="jpeg", quality=80)
        dst = img.resize((512, 512))
        img.save(
            os.path.join(path, str(uid) + "_512" + ".jpg"), format="jpeg", quality=80
        )
        dst = img.resize((256, 256))
        dst.save(
            os.path.join(path, str(uid) + "_256" + ".jpg"), format="jpeg", quality=80
        )
        dst = img.resize((50, 50))
        dst.save(
            os.path.join(path, str(uid) + "_50" + ".jpg"), format="jpeg", quality=80
        )

        instance.profilepic = os.path.join(
            "profilepic", str(instance.id), str(uid) + ".jpg"
        )

        post_save.disconnect(resize_image, sender=settings.AUTH_USER_MODEL)
        instance.save()
        post_save.connect(resize_image, sender=settings.AUTH_USER_MODEL)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
