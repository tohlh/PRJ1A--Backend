# Generated by Django 4.0.3 on 2022-04-10 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('driver', '0001_initial'),
        ('passenger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger_lat', models.FloatField()),
                ('passenger_long', models.FloatField()),
                ('start_POI_name', models.CharField(max_length=150)),
                ('start_POI_address', models.CharField(max_length=150)),
                ('start_POI_lat', models.FloatField()),
                ('start_POI_long', models.FloatField()),
                ('end_POI_name', models.CharField(max_length=150)),
                ('end_POI_address', models.CharField(max_length=150)),
                ('end_POI_lat', models.FloatField()),
                ('end_POI_long', models.FloatField()),
                ('before_pickup_path', models.TextField()),
                ('after_pickup_path', models.TextField()),
                ('distance', models.DecimalField(decimal_places=2, default='0', max_digits=6)),
                ('est_price', models.DecimalField(decimal_places=2, default='0', max_digits=6)),
                ('real_price', models.DecimalField(decimal_places=2, default='0', max_digits=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.PositiveIntegerField()),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='driver.driver')),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='passenger.passenger')),
            ],
        ),
    ]