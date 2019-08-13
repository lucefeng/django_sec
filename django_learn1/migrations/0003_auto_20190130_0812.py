# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_learn1', '0002_usermodels'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodels',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='usermodels',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='UserModels',
        ),
    ]
