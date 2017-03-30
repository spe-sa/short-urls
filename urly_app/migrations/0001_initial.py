# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('short_code', models.SlugField(serialize=False, primary_key=True)),
                ('canonical', models.URLField()),
                ('fragment', models.SlugField()),
                ('tracking', models.URLField()),
                ('pub_user', models.SlugField()),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('hit_count', models.IntegerField(default=0)),
            ],
        ),
    ]
