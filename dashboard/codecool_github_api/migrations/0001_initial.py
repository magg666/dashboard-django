# Generated by Django 2.2.5 on 2019-09-06 11:05

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(choices=[('PB', 'ProgBasic Module'), ('WEB', 'Web & SQL'), ('OOP', 'Object Orientated Programming Module'), ('ADV', 'Advanced Module')], max_length=5)),
            ],
            options={
                'db_table': 'module',
            },
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('url', models.URLField()),
                ('plan', models.URLField()),
                ('owner', models.CharField(max_length=100)),
                ('project', models.CharField(max_length=100)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='codecool_github_api.Module')),
            ],
            options={
                'db_table': 'repository',
            },
            managers=[
                ('current', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.DateField()),
                ('contributor', models.CharField(max_length=100)),
                ('commits', models.IntegerField()),
                ('additions', models.IntegerField()),
                ('deletions', models.IntegerField()),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='codecool_github_api.Repository')),
            ],
            options={
                'db_table': 'weekly_statistic',
            },
        ),
        migrations.CreateModel(
            name='TotalStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commits', models.IntegerField()),
                ('additions', models.IntegerField()),
                ('deletions', models.IntegerField()),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='total', to='codecool_github_api.Repository')),
            ],
            options={
                'db_table': 'statistic',
            },
        ),
        migrations.AddIndex(
            model_name='repository',
            index=models.Index(fields=['date', 'url'], name='repository_date_135884_idx'),
        ),
    ]
