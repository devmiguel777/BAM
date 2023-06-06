# Generated by Django 4.2 on 2023-06-06 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_page_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='metatagcompany',
            name='meta_tag_content',
            field=models.CharField(default='content', max_length=255, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='metatagcompany',
            name='meta_tag_property',
            field=models.CharField(default='property', max_length=255, verbose_name='Property'),
        ),
    ]