# Generated by Django 4.0.5 on 2023-06-23 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0016_alter_userprocedure_type_procedure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprocedure',
            name='type_procedure',
            field=models.CharField(choices=[('pre_op', 'Pré-1operatório'), ('pos_op', 'Pós-operatório')], default='pre_op', max_length=20, null=True),
        ),
    ]
