from datetime import date
from dateutil.relativedelta import relativedelta, SU
from rest_framework import serializers

from .models import Module, Repository, WeeklyStatistic, TotalStatistic


class CurrentWeekSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        today = date.today()
        last_sunday = today + relativedelta(weekday=SU(-1))
        data = data.filter(week__range=[last_sunday, today])
        data = data.exclude(commits=0)
        return super().to_representation(data)


class ExistWeekStatsSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.exclude(users__isnull=True)
        return super().to_representation(data)


# serializers for weekly GitHub statistics
class WeekDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyStatistic
        fields = ['contributor', 'commits']
        list_serializer_class = CurrentWeekSerializer


class WeekProjectsSerializer(serializers.ModelSerializer):
    users = WeekDataSerializer(many=True, read_only=True)
    project = serializers.SerializerMethodField()

    class Meta:
        model = Repository
        fields = ['project', 'users']
        list_serializer_class = ExistWeekStatsSerializer

    @staticmethod
    def get_project(obj):
        return obj.project.replace('-', ' ').title() if obj.project else None


class WeekSerializer(serializers.ModelSerializer):
    qs = Repository.current.all()
    projects = WeekProjectsSerializer(instance=qs, many=True, read_only=True)
    module = serializers.SerializerMethodField()

    @staticmethod
    def get_module(obj):
        return obj.get_module_display()

    class Meta:
        model = Module
        fields = ['module', 'projects']


# serializers for overall statistics

class ExistTotalSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.exclude(total__isnull=True)
        return super().to_representation(data)


class TotalDataSerializer(serializers.ModelSerializer):
    """
    Serialize overall statistics
    """

    class Meta:
        model = TotalStatistic
        fields = ['commits', 'additions', 'deletions']


class TotalProjectsSerializer(serializers.ModelSerializer):
    total = TotalDataSerializer(many=True, read_only=True)
    project = serializers.SerializerMethodField()

    class Meta:
        model = Repository
        fields = ['project', 'total']
        list_serializer_class = ExistTotalSerializer

    @staticmethod
    def get_project(obj):
        return obj.project.replace('-', ' ').title() if obj.project else None


class TotalSerializer(serializers.ModelSerializer):
    qs = Repository.current.all()
    projects = TotalProjectsSerializer(instance=qs, many=True, read_only=True)
    module = serializers.SerializerMethodField()

    @staticmethod
    def get_module(obj):
        return obj.get_module_display()

    class Meta:
        model = Module
        fields = ['module', 'projects']
