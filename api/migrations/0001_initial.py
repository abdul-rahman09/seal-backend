# Generated by Django 3.2.14 on 2022-07-11 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('download', models.IntegerField(default=0)),
                ('rdoc', models.FileField(blank=True, upload_to='rdocs')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LinkToDownload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expire', models.DateTimeField()),
                ('link', models.CharField(default='', max_length=100)),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.document')),
            ],
        ),
    ]
