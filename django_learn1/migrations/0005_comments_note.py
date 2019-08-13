# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_learn1', '0004_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments_Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('hcontent', models.CharField(max_length=1000)),
                ('h_time', models.DateTimeField(auto_now=True)),
                ('hname', models.ForeignKey(to='django_learn1.User')),
            ],
        ),
    ]
