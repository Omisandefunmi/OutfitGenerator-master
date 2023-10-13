# Generated by Django 4.2.3 on 2023-08-11 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Outfits', '0006_remove_clothingitem_user_styleone_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothingitem',
            name='category',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='clothingitem',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='possibleitem',
            name='category',
            field=models.CharField(default='upper', max_length=100),
        ),
        migrations.AlterField(
            model_name='styleone',
            name='category',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='styleone',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='styleone',
            name='season',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='stylethree',
            name='category',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='stylethree',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='stylethree',
            name='season',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='styletwo',
            name='category',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='styletwo',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='styletwo',
            name='season',
            field=models.CharField(max_length=100),
        ),
    ]