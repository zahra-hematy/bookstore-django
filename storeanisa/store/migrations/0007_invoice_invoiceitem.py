# Generated by Django 4.0.5 on 2022-07-24 04:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0006_bookrequest_contact_alter_book_cover_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('total', models.IntegerField(default=0)),
                ('state', models.CharField(choices=[('pending', 'Pending'), ('done', 'Done')], default='pending', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('count', models.ImageField(default=1, upload_to='')),
                ('title', models.CharField(max_length=255)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.book')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.invoice')),
            ],
        ),
    ]
