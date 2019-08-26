from .models import Repository
import os
import requests


def get_github_statistics() -> str or list:
    """
    Fetches data from github api for active projects.
    Adds id of repository to data.

    :return:
        message: str - if error occurs
        data: list of json-encoded github statistics

    """
    token = os.environ.get("TOKEN")
    head = {'Authorization': 'token {}'.format(token)}
    active_repositories = Repository.current.all()
    processed_data = []

    for repository in active_repositories:
        owner = repository.owner
        project = repository.project
        url = f'https://api.github.com/repos/{owner}/{project}/stats/contributors'
        try:
            response = requests.get(url, headers=head)

            if not response.status_code // 100 == 2:
                return f"Error: Unexpected response {response}"

            repository_statistic = response.json()
            for data in repository_statistic:
                data['repository_id'] = repository.id
            processed_data.append(repository_statistic)

        except requests.exceptions.RequestException as e:
            return f"Serious error: {e}"

    return processed_data
