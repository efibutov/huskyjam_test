# Generated by Django 2.2 on 2019-04-09 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Technician',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_model', models.CharField(choices=[('Toyota', 'Toyota'), ('Mazda', 'Mazda'), ('Hyundai', 'Hyundai'), ('Honda', 'Honda'), ('Buick', 'Buick')], max_length=50)),
                ('client_first_name', models.CharField(max_length=50)),
                ('client_last_name', models.CharField(max_length=50)),
                ('date_time', models.DateTimeField()),
                ('technician', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meeting', to='garage.Technician')),
            ],
        ),
    ]
