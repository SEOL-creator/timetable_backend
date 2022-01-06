import os
import uuid
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from PIL import Image

from .models import ArticlePhoto


@receiver(post_save, sender=ArticlePhoto)
def resize_image(sender, instance=None, update_fields=None, **kwargs):
    photo = instance.photo
    fullpath = photo.path
    path = os.path.dirname(fullpath)
    extension = os.path.splitext(fullpath)[1]
    uid = uuid.uuid4()
    article_id = instance.article.id

    img = Image.open(fullpath).convert("RGB")
    width, height = img.size

    square_img = None

    if width > height:
        instance.orientation = "HORIZONTAL"
        square_img = img.crop(
            (
                round((width - height) / 2),
                0,
                height + round((width - height) / 2),
                height,
            )
        )
    elif height > width:
        instance.orientation = "VERTICAL"
        square_img = img.crop(
            (
                0,
                round((height - width) / 2),
                width,
                width + round((height - width) / 2),
            )
        )
    else:
        instance.orientation = "SQUARE"
        square_img = img

    img.save(os.path.join(path, str(uid) + ".jpg"), format="jpeg", quality=80)
    square_img.resize((512, 512)).save(
        os.path.join(path, str(uid) + "_square" + ".jpg"), format="jpeg", quality=80
    )

    instance.photo = os.path.join("article_photos", str(article_id), str(uid) + ".jpg")
    instance.width = width
    instance.height = height

    post_save.disconnect(resize_image, sender=ArticlePhoto)
    instance.save()
    post_save.connect(resize_image, sender=ArticlePhoto)
