# Generated by Django 4.1.2 on 2022-10-09 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('village_name', models.CharField(blank=True, max_length=50, null=True)),
                ('district_name', models.CharField(blank=True, max_length=50, null=True)),
                ('state_name', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeleguFarmerDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('village_name', models.CharField(blank=True, max_length=50, null=True)),
                ('district_name', models.CharField(blank=True, max_length=50, null=True)),
                ('state_name', models.CharField(blank=True, max_length=50, null=True)),
                ('farmer', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='te', to='Farmer.farmer')),
            ],
        ),
        migrations.CreateModel(
            name='PunjabiFarmerDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('village_name', models.CharField(blank=True, max_length=50, null=True)),
                ('district_name', models.CharField(blank=True, max_length=50, null=True)),
                ('state_name', models.CharField(blank=True, max_length=50, null=True)),
                ('farmer', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='pu', to='Farmer.farmer')),
            ],
        ),
        migrations.CreateModel(
            name='MarathiFarmerDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('village_name', models.CharField(blank=True, max_length=50, null=True)),
                ('district_name', models.CharField(blank=True, max_length=50, null=True)),
                ('state_name', models.CharField(blank=True, max_length=50, null=True)),
                ('farmer', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='ma', to='Farmer.farmer')),
            ],
        ),
        migrations.CreateModel(
            name='HindiFarmerDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('village_name', models.CharField(blank=True, max_length=50, null=True)),
                ('district_name', models.CharField(blank=True, max_length=50, null=True)),
                ('state_name', models.CharField(blank=True, max_length=50, null=True)),
                ('farmer', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='hi', to='Farmer.farmer')),
            ],
        ),
    ]
