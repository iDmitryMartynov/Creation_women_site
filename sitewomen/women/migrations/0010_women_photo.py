# Generated by Django 5.1.1 on 2024-10-13 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0009_uploadfiles_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='women',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]