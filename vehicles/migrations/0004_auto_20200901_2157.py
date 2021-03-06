# Generated by Django 3.1 on 2020-09-01 18:57

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('vehicles', '0003_vehicle_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('enterprise', models.ManyToManyField(to='vehicles.Enterprise')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('salary', models.FloatField()),
                ('is_active', models.BooleanField()),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicles.enterprise')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicles.vehicle')),
            ],
        ),
        migrations.AddField(
            model_name='vehicle',
            name='enterprise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicles.enterprise'),
        ),
    ]
