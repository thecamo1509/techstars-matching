# Generated by Django 3.1.5 on 2021-01-28 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_mentor_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='mentorPic',
            field=models.ImageField(default='hakkea.png', upload_to=''),
            preserve_default=False,
        ),
    ]
