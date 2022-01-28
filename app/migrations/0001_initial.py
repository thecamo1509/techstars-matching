# Generated by Django 2.2.10 on 2022-01-27 20:27

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Startup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(max_length=200)),
                ('whatwedo', models.CharField(max_length=400)),
                ('startupPic', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=200)),
                ('day', models.CharField(choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('undefined', 'Undefined')], max_length=200)),
                ('timeSlot', models.CharField(choices=[('AM', 'Morning'), ('PM', 'Afternoon'), ('undefined', 'Undefined')], max_length=50)),
                ('mentorPic', models.URLField()),
                ('startup', models.ManyToManyField(to='app.Startup')),
            ],
        ),
        migrations.CreateModel(
            name='LeadMentor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mentor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Mentor')),
                ('startup', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Startup')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('endtime', models.TimeField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in progress', 'In Progress'), ('completed', 'Completed')], max_length=50)),
                ('mentorResponse', models.CharField(blank=True, choices=[('want', 'Want'), ('wont', 'Wont'), ('willing', 'Willing')], max_length=200)),
                ('startupResponse', models.CharField(blank=True, choices=[('want', 'Want'), ('wont', 'Wont'), ('willing', 'Willing')], max_length=200)),
                ('mentorNotes', models.CharField(blank=True, max_length=10000)),
                ('startupNotes', models.CharField(blank=True, max_length=10000)),
                ('mentorRank', models.IntegerField(blank=True, null=True)),
                ('startupRank', models.IntegerField(blank=True, null=True)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Mentor')),
                ('startup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Startup')),
            ],
        ),
        migrations.CreateModel(
            name='AdHocMentor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mentor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Mentor')),
                ('startups', models.ManyToManyField(to='app.Startup')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('profile_pic', models.ImageField(upload_to='')),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'startup'), (2, 'mentor'), (3, 'staff')], default=3, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
