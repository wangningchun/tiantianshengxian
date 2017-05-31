# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FreshInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fname', models.CharField(max_length=20)),
                ('fpwd', models.CharField(max_length=40)),
                ('femail', models.CharField(max_length=30)),
                ('frecipients', models.CharField(default=b'', max_length=20)),
                ('faddress', models.CharField(default=b'', max_length=100)),
                ('fyoubian', models.CharField(default=b'', max_length=10)),
                ('fphone', models.CharField(default=b'', max_length=20)),
            ],
        ),
    ]
