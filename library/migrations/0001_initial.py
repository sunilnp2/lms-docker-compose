# Generated by Django 5.0.1 on 2024-01-30 16:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('isbn', models.CharField(max_length=13, unique=True)),
                ('published_date', models.DateField()),
                ('genre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BookDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_pages', models.PositiveIntegerField()),
                ('publisher', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=50)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='library.book')),
            ],
        ),
        migrations.CreateModel(
            name='BorrowedBooks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowed_date', models.DateField(auto_now_add=True)),
                ('returned_date', models.DateField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
