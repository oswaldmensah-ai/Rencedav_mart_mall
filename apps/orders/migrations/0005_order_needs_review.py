from django.db import migrations, models


def mark_existing_orders_reviewed(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    Order.objects.all().update(needs_review=False)


class Migration(migrations.Migration):
    dependencies = [
        ('orders', '0004_order_delivery_special_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='needs_review',
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(mark_existing_orders_reviewed, migrations.RunPython.noop),
    ]
