# Generated by Django 4.0.5 on 2022-07-13 12:20

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_book_cover'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='request_covers/')),
                ('number_of_requests', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=store.models.get_covert_path),
        ),
        migrations.AddConstraint(
            model_name='bookrequest',
            constraint=models.UniqueConstraint(fields=('name', 'author'), name='name_author_uniq'),
        ),
    ]