# Generated by Django 4.1.4 on 2023-07-13 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watch', '0005_delete_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watch_type', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]
