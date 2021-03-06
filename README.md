# Codecool Dashboard I
> Backend part of project Codecool Dashboard.
Project gets projects' data from [Codecool](https://codecool.com/pl/) students and delivers statistics about repositories in JSON format.

Project was created to practice back-end skills:
* Working with Django and REST framework using OOP based approach
* Celery and RabbitMQ supports asynchronous task queue based on distributed message passing.
* PostgreSQL as database source

Codecool Dashboard uses:
* Class based views in Django
* Django Rest Framework serializers
* Custom written migrations for Django
* Django ORM
* External Apis
* Cyclic tasks supervised by Celery and RabbitMq
* Custom form validation



## Table of contents
* [General info](#general-info)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Setup](#setup)
* [Code Examples](#code-examples)
* [Status](#status)
* [Inspiration](#inspiration)
* [Contact](#contact)

## General info
Codecool Dashboard:
* Shows on main page instruction and list of projects
* Displays form to add project's data
* Gets and processes data for repository from github on weekly basis and as a whole
* Serves processed data in JSON format
Second part (frontend) you can find [here](https://github.com/magg666/dashboard-react)

## Screenshots
Main page:

![Main page](./dashboard-b1.png)

Form page:

![Form page](./dashboard-b2.png)

JSON response:

![JSON response](./dashboard-b3.png)

## Technologies
* Django - version 2.2.5
* Django Rest Framework - version 3.10.3
* Postgresql
* RabbitMQ - version 0.2.0
* Celery - version 4.3.0
* html, css, bootstrap

## Setup
Use requirements.txt to download all nedeed dependencies, run the manage.py.

## Code Examples
Using signals in Django:
```python
@receiver(post_save, sender=Repository)
def repository_owner(instance, created, **kwargs):
    if created:
        owner = str(instance.url).split("//")[NO_SCHEME_INDEX].split("/")[OWNER_INDEX]
        Repository.objects.filter(pk=instance.pk).update(owner=owner)
```
Custom form validation:
```python
    def clean_url(self) -> dict:
        """ Method to validate link to GitHub repository. It checks domain and necessary content
        :raise
            Validation Error
        :return:
            data: dict - processed and validated data from form
        """
        # link to repository is splited to list:
        #   first split by '//' = [https, github.com/OWNER/PROJECT_NAME]
        #   second split by '/' = [github.com, OWNER, PROJECT]

        url_without_schema_index = 1
        domain_index = 0
        github_domain = "github.com"
        data = self.cleaned_data['url']

        if str(data).split("//")[url_without_schema_index].split("/")[domain_index] != github_domain:
            raise ValidationError("Repository url must be from GitHub")

        if len(str(data).split("//")[url_without_schema_index].split("/")) < 3:
            raise ValidationError(
                "Link to repository must contain github.com domain, name of owner and repository name separated by '/'")

        return data
```
Self-written migrations:
```python

def insert_modules(apps, schema_editor):
    Module = apps.get_model('codecool_github_api', 'Module')
    modules_list = ['PB', 'WEB', 'OOP', 'ADV']
    for shortcut in modules_list:
        new_module = Module(module=shortcut)
        new_module.save()


class Migration(migrations.Migration):
    dependencies = [
        ('codecool_github_api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_modules)
    ]
```

## Status
Project is finished, but I do not exclude the possibility of further developments.

## Inspiration
Credits for:

[Maciej Jankowski](https://github.com/maciejjankowski) - Codecool mentor - for idea and help. Thank you.

All Codecool mentors and student.

[This beautiful css animation by Kacper Parzęcki](https://codepen.io/kacpertn4t/pen/RYzZwG)

And, of course and as always - StackOverflow... :)

## Contact
Created by [Magda Wąsowicz](mailto:mw23127@gmail.com) - feel free to contact me!
