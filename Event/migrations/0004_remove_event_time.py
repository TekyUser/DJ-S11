# Generated by Django 5.1.1 on 2024-12-31 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Event", "0003_alter_event_time"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="time",
        ),
    ]