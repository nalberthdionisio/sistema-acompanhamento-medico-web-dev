

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0010_remove_procedure_type_procedure_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprocedure',
            name='type_procedure',

            field=models.CharField(choices=[('pre_op', 'Pré-1operatório'), ('pos_op', 'Pós-operatório')], max_length=20, null=True),
        ),
    ]
