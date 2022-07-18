# Generated by Django 2.2.24 on 2022-07-17 23:28

from django.db import models, migrations


def find_duplicates(apps, schema_editor):

    List = apps.get_model("lists", "List")

    for list_ in List.objects.all():

        items = list_.item_set.all()
        texts = set()

        for i, item in enumerate(items):

            if item.text in texts:

                item.text = f"{item.text} ({i})"
                item.save()

            texts.add(item.text)

class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_item_list'),
    ]

    operations = [
        migrations.RunPython(find_duplicates)
    ]