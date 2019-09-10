from django.contrib import admin

from .models import Module, Repository, WeeklyStatistic, TotalStatistic

admin.site.register(Module)
admin.site.register(Repository)
admin.site.register(WeeklyStatistic)
admin.site.register(TotalStatistic)
