# Generated by Django 4.2 on 2023-05-11 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watch', '0003_delete_watch'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('logo', models.ImageField(upload_to='shp/images')),
            ],
        ),
    ]
