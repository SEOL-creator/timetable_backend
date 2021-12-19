from django.db import models


class FrontVersion(models.Model):
    version = models.CharField(max_length=10)
    note = models.TextField(blank=True)

    def __str__(self):
        return self.version
