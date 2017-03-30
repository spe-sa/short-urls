# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0023_auto_20161209_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='accounting_code',
            field=models.CharField(help_text=b'Optional: the accounting code to associate with this short URL, for time and expenses, e.g., EZLabor code', max_length=18, blank=True),
        ),
    ]
