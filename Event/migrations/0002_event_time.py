# Generated by Django 5.1.1 on 2024-12-31 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Event", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="time",
            field=models.TimeField(default="00:00:00"),
        ),
    ]
