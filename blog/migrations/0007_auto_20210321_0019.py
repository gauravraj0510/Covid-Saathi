# Generated by Django 3.1.4 on 2021-03-20 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20210321_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='bedrequest',
            name='address',
            field=models.CharField(default=1212, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bedrequest',
            name='phone_number',
            field=models.IntegerField(default=1212, max_length=10),
            preserve_default=False,
        ),
    ]
