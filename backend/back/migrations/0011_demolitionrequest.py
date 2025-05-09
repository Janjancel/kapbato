# Generated by Django 5.1.5 on 2025-03-10 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0010_remove_userprofile_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemolitionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('where', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='demolition_images/')),
            ],
        ),
    ]
