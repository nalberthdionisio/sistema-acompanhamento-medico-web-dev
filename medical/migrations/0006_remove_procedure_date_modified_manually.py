# Generated by Django 4.0.5 on 2023-05-26 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0005_procedure_date_modified_manually'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='procedure',
            name='date_modified_manually',
        ),
    ]
