# Generated by Django 5.0.6 on 2024-07-14 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updated', '0003_cie_sub_code_student_usn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marks',
            name='attendance',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='marks',
            name='marks',
            field=models.IntegerField(null=True),
        ),
    ]