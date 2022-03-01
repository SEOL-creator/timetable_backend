from django.contrib import admin
from .models import *

admin.site.register(Timetable)
admin.site.register(TimetableItem)
admin.site.register(StaticClass)
admin.site.register(FlexibleClass)
admin.site.register(ClassTimetableMaster)
admin.site.register(ClassTimetableItem)
admin.site.register(ClassTimetableTempItem)
