# Generated by Django 2.0 on 2018-01-12 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name_t', models.CharField(db_index=True, max_length=200)),
                ('slug_t', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'db_tablespace': '',
                'verbose_name': 'category Translation',
                'db_table': 'shop_category_translation',
                'default_permissions': (),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ProductTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name_t', models.CharField(db_index=True, max_length=200)),
                ('slug_t', models.SlugField(max_length=200)),
                ('description_t', models.TextField(blank=True)),
            ],
            options={
                'db_tablespace': '',
                'verbose_name': 'product Translation',
                'db_table': 'shop_product_translation',
                'default_permissions': (),
                'managed': True,
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterIndexTogether(
            name='product',
            index_together=set(),
        ),
        migrations.AddField(
            model_name='producttranslation',
            name='master',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='shop.Product'),
        ),
        migrations.AddField(
            model_name='categorytranslation',
            name='master',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='shop.Category'),
        ),
        migrations.AlterUniqueTogether(
            name='producttranslation',
            unique_together={('language_code', 'master')},
        ),
        migrations.AlterUniqueTogether(
            name='categorytranslation',
            unique_together={('language_code', 'master')},
        ),
    ]