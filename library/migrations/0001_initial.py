# Generated by Django 2.2 on 2021-02-15 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=20, verbose_name='Фамилия')),
                ('birth_year', models.IntegerField(verbose_name='Год рождения')),
            ],
            options={
                'verbose_name': 'автор',
                'verbose_name_plural': 'авторы',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('isbn', models.IntegerField(verbose_name='ISBN')),
                ('publication_year', models.IntegerField(verbose_name='Год издания')),
                ('sheets_number', models.IntegerField(verbose_name='Количество страниц')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='library.Author', verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'книга',
                'verbose_name_plural': 'книги',
            },
        ),
    ]