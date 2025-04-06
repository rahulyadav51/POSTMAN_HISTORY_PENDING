# Generated by Django 5.1.7 on 2025-04-06 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APIRequestHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('method', models.CharField(max_length=10)),
                ('headers', models.TextField(blank=True)),
                ('body_type', models.CharField(max_length=30)),
                ('raw_body', models.TextField(blank=True, null=True)),
                ('formdata', models.JSONField(blank=True, null=True)),
                ('urlencoded', models.JSONField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
