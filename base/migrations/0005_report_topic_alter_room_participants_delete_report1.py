# Generated by Django 4.0.1 on 2022-04-18 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_room_participants_report1_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.topic'),
        ),
        migrations.AlterField(
            model_name='room',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Report1',
        ),
    ]
