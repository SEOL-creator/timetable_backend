from django.db import models


class Schedule(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    is_registered_dday = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("start_date",)
