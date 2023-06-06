# Generated by Django 4.2.1 on 2023-06-06 21:22

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('common_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('cpf', models.CharField(max_length=11)),
                ('gender', models.IntegerField(choices=[(0, 'Male'), (1, 'Famale'), (2, 'Other')])),
                ('birth', models.DateField()),
            ],
            options={
                'db_table': 'User',
                'ordering': ['date_joined'],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('commonuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.commonuser')),
            ],
            options={
                'db_table': 'Customer',
            },
            bases=('users.commonuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('commonuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.commonuser')),
            ],
            options={
                'db_table': 'Seller',
            },
            bases=('users.commonuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Phones',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('number', models.CharField(max_length=10, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='phones', to='users.commonuser')),
            ],
        ),
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('neighborhood', models.CharField(max_length=100, null=True)),
                ('number', models.CharField(max_length=100, null=True)),
                ('complement', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adresses', to='users.commonuser')),
            ],
        ),
    ]
