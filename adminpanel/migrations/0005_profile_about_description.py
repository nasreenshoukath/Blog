# Generated by Django 5.0.6 on 2024-07-27 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0004_comment_is_hidden_alter_blog_blog_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about_description',
            field=models.TextField(default='Your default description here'),
        ),
    ]