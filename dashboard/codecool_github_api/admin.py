from django.contrib import admin

from .models import Module, Repository, WeeklyStatistic, TotalStatistic

admin.register(Module)
admin.register(Repository)
admin.register(WeeklyStatistic)
admin.register(TotalStatistic)
