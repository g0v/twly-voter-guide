# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Standpoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=32, db_index=True)),
                ('vote', models.ForeignKey(related_name='standpoints', to='vote.Vote', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_Standpoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opinion', models.CharField(max_length=32, db_index=True)),
                ('standpoint', models.ForeignKey(to='standpoint.Standpoint')),
                ('user', models.ForeignKey(related_name='standpoints', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='user_standpoint',
            unique_together=set([('standpoint', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='standpoint',
            unique_together=set([('title', 'vote')]),
        ),
    ]
