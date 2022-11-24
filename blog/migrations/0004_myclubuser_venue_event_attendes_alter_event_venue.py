# Generated by Django 4.0.4 on 2022-05-18 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_event_delete_opi'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyClubUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('email_adress', models.EmailField(max_length=120, verbose_name='Email')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Event name')),
                ('adress', models.CharField(max_length=120)),
                ('zip_code', models.CharField(max_length=120, verbose_name='Zip_code')),
                ('phone', models.CharField(max_length=120, verbose_name='Phone')),
                ('web', models.URLField(max_length=120, verbose_name='Website adress')),
                ('email_adress', models.EmailField(max_length=120, verbose_name='Email')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='attendes',
            field=models.ManyToManyField(blank=True, to='blog.myclubuser'),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.venue'),
        ),
    ]
