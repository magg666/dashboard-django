from datetime import date
from .models import WeeklyStatistic, TotalStatistic
from .utils import get_github_statistics
from celery import shared_task


# This task is set to execute from Monday to Friday, every 5 minutes
@shared_task()
def save_github_weekly_statistic() -> None:
    """
    Updates or creates github weekly statistic data for active repositories

    :return: None
    """
    repositories_data = get_github_statistics()
    last_week_index = -1

    for repository in repositories_data:

        for data in repository:
            contributor = data['author']['login']
            repository_id = data['repository_id']
            week = date.fromtimestamp(data['weeks'][last_week_index]['w'])
            additions = data['weeks'][last_week_index]['a']
            deletions = data['weeks'][last_week_index]['d']
            commits = data['weeks'][last_week_index]['c']

            WeeklyStatistic.objects.all().update_or_create(repository_id=repository_id,
                                                           contributor=contributor,
                                                           week=week,
                                                           defaults={"commits": commits,
                                                                     "additions": additions,
                                                                     'deletions': deletions})

# This task is set to execute on Friday between 9-15 every hour
@shared_task()
def save_github_total_statistic() -> None:
    """
    Updates or creates github total statistic data for project repository

    :return: None
    """
    repositories_data = get_github_statistics()

    for repository in repositories_data:
        repository_id = repository['repository_id']
        commits = sum(data['total'] for data in repository)
        additions = 0
        deletions = 0

        for data in repository:
            weeks = data['weeks']
            additions += sum(item['a'] for item in weeks)
            deletions += sum(item['d'] for item in weeks)

            TotalStatistic.objects.all().update_or_create(repository_id=repository_id,
                                                          defaults={'commits': commits,
                                                                    'additions': additions,
                                                                    'deletions': deletions})



