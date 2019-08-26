from django.contrib import admin
from .models import Repository, WeeklyStatistic, TotalStatistic

admin.register(Repository)
admin.register(WeeklyStatistic)
admin.register(TotalStatistic)
