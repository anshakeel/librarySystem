# Generated by Django 2.2.7 on 2021-11-22 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20211121_2112'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='copy',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='print',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='rent',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='stock',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='write',
            unique_together=set(),
        ),
    ]
