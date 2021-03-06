# Generated by Django 3.1.4 on 2021-04-03 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0013_post_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='proof',
            field=models.ImageField(default='default.png', upload_to='hosp_proofs'),
        ),
        migrations.AddField(
            model_name='post',
            name='type',
            field=models.CharField(default='Dedicated covid hospital', max_length=100),
        ),
        migrations.CreateModel(
            name='Hosp_Img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img1', models.ImageField(default='default.jpg', upload_to='hosp_imgs')),
                ('img2', models.ImageField(default='default.jpg', upload_to='hosp_imgs')),
                ('img3', models.ImageField(default='default.jpg', upload_to='hosp_imgs')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
