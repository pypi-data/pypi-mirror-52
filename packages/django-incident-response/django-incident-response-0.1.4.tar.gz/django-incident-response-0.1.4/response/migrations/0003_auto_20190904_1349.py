# Generated by Django 2.2.3 on 2019-09-04 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('response', '0002_timelineevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='pinnedmessage',
            name='timeline_event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='response.TimelineEvent'),
        ),
        migrations.AlterField(
            model_name='timelineevent',
            name='event_type',
            field=models.CharField(help_text='Type of event.', max_length=10),
        ),
    ]
