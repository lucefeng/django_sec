# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_learn1', '0009_auto_20190619_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments_note',
            name='hname',
            field=models.ForeignKey(default='1@1.com', to='django_learn1.User', to_field='email'),
        ),
    ]
