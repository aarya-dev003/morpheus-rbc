# Generated by Django 5.1.4 on 2025-01-04 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_answer_answer_text'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Response',
            new_name='FormResponse',
        ),
    ]