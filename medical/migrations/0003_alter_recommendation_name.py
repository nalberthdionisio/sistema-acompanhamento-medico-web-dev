# Generated by Django 4.0.5 on 2023-05-15 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0002_users_association'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
