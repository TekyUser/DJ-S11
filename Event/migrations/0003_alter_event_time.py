# Generated by Django 5.1.1 on 2024-12-31 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Event", "0002_event_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="time",
            field=models.TimeField(default="00:00:00"),
        ),
    ]