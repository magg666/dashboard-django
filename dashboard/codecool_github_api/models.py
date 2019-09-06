from datetime import date
from dateutil.relativedelta import relativedelta, MO
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Module(models.Model):
    """
    Students' learning stage
    """
    objects = models.Manager()

    MODULES = [
        ('PB', 'ProgBasic Module'),
        ('WEB', 'Web & SQL'),
        ('OOP', 'Object Orientated Programming Module'),
        ('ADV', 'Advanced Module')]

    module = models.CharField(max_length=5, choices=MODULES)

    class Meta:
        db_table = 'module'

    def __str__(self):
        return self.get_module_display()


class RepositoryManager(models.Manager):
    """
    Manager to filter only active repositories.
    Active repositories are define as added on or after last Monday
    """

    def get_queryset(self) -> dict:
        """
        Filters all Repository data by date. Chooses active repositories.
        :return:
            queryset: dict - collections of database queries
        """

        # define today's date
        today = date.today()

        # find last monday (if today is monday - it chooses today)
        last_monday = today + relativedelta(weekday=MO(-1))

        # find all records, which date is equal or bigger then last monday
        return super().get_queryset().filter(date__range=[last_monday, today])


class Repository(models.Model):
    """
    Model Repository contain data about work of CodeCool's students.
    Fields:
        date - date of adding record;
        url - link to github repository for project
        plan - link to plan for project
        owner - project owner login
        project - project name
        module - current module of students. Foreign key to Module.

    Methods:
        __str__

    """
    current = RepositoryManager()
    objects = models.Manager()

    class Meta:
        db_table = 'repository'
        indexes = [
            models.Index(fields=['date', 'url']),
        ]

    # fields
    date = models.DateField(auto_now=True)
    url = models.URLField()
    plan = models.URLField()
    owner = models.CharField(max_length=100, name="owner")
    project = models.CharField(max_length=100, name='project')
    module = models.ForeignKey(Module, related_name='projects', on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Method to string
        :return:
            project name: str
        """

        return str(self.project)


# signals for Repository Model
NO_SCHEME_INDEX = 1
OWNER_INDEX = 1
PROJECT_INDEX = 2


@receiver(post_save, sender=Repository)
def repository_owner(instance, created, **kwargs):
    if created:
        owner = str(instance.url).split("//")[NO_SCHEME_INDEX].split("/")[OWNER_INDEX]
        Repository.objects.filter(pk=instance.pk).update(owner=owner)


@receiver(post_save, sender=Repository)
def repository_project(instance, created, **kwargs):
    if created:
        project = str(instance.url).split("//")[NO_SCHEME_INDEX].split("/")[PROJECT_INDEX]
        Repository.objects.filter(pk=instance.pk).update(project=project)


class WeeklyStatistic(models.Model):
    """
    Summarized data about each active repository on a weekly basis.
    Keeps data about current week contributors' commits, deletions and additions
    Fields:
        repository - ForeignKey Repository;
        week - date from timestamp;
        contributor - login of project contributor;
        commits - amount of commits for given contributor;
        additions - amount of additions for given contributor
        deletions - amount of deletions for given contributor

    Methods
        __str__
    """
    objects = models.Manager()  # default

    class Meta:
        db_table = 'weekly_statistic'

    # fields
    repository = models.ForeignKey(Repository, related_name='users', on_delete=models.CASCADE)
    week = models.DateField()
    contributor = models.CharField(max_length=100)
    commits = models.IntegerField()
    additions = models.IntegerField()
    deletions = models.IntegerField()

    def __str__(self) -> str:
        """
        Method to string
        :return:
            project name and contributor : str

        """
        return f'{self.repository.__str__()}: {self.contributor}'


class TotalStatistic(models.Model):
    """
    Summarized data about each active repository.
    Keeps data about total statistic for project
    Fields:
        repository - ForeignKey Repository;
        commits - amount of commits for project;
        additions - amount of additions for project;
        deletions - amount of deletions for project;

    Methods
        __str__
    """
    objects = models.Manager()  # default

    class Meta:
        db_table = 'statistic'

    # fields
    repository = models.ForeignKey(Repository, related_name='total', on_delete=models.CASCADE)
    commits = models.IntegerField()
    additions = models.IntegerField()
    deletions = models.IntegerField()

    def __str__(self) -> str:
        """
        Method to string
        :return:
            project name and contributor : str

        """
        return f'{self.repository.__str__()}: {self.commits}'
