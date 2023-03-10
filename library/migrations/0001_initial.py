# Generated by Django 4.1.6 on 2023-02-10 07:46

from django.db import migrations, models
import library.models.author


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('surname', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('phone', models.IntegerField()),
                ('fb_name', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(null=True, upload_to=library.models.author.recipe_image_file_path)),
            ],
            options={
                'unique_together': {('name', 'surname')},
            },
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('book_pages', models.PositiveIntegerField()),
                ('genre', models.PositiveIntegerField()),
                ('release_date', models.DateField()),
                ('author', models.ManyToManyField(to='library.author')),
            ],
        ),
    ]
