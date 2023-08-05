# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-08 15:50
from __future__ import unicode_literals

import django_extensions.db.fields.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa_stripe', '0011_auto_20170907_1201'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stripewebhook',
            options={'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='stripecoupon',
            name='amount_off',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Amount (in the currency specified) that will be taken off the subtotal of any invoices for thiscustomer.', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stripecoupon',
            name='currency',
            field=models.CharField(blank=True, choices=[('usd', 'USD'), ('aed', 'AED'), ('afn', 'AFN'), ('all', 'ALL'), ('amd', 'AMD'), ('ang', 'ANG'), ('aoa', 'AOA'), ('ars', 'ARS'), ('aud', 'AUD'), ('awg', 'AWG'), ('azn', 'AZN'), ('bam', 'BAM'), ('bbd', 'BBD'), ('bdt', 'BDT'), ('bgn', 'BGN'), ('bif', 'BIF'), ('bmd', 'BMD'), ('bnd', 'BND'), ('bob', 'BOB'), ('brl', 'BRL'), ('bsd', 'BSD'), ('bwp', 'BWP'), ('bzd', 'BZD'), ('cad', 'CAD'), ('cdf', 'CDF'), ('chf', 'CHF'), ('clp', 'CLP'), ('cny', 'CNY'), ('cop', 'COP'), ('crc', 'CRC'), ('cve', 'CVE'), ('czk', 'CZK'), ('djf', 'DJF'), ('dkk', 'DKK'), ('dop', 'DOP'), ('dzd', 'DZD'), ('egp', 'EGP'), ('etb', 'ETB'), ('eur', 'EUR'), ('fjd', 'FJD'), ('fkp', 'FKP'), ('gbp', 'GBP'), ('gel', 'GEL'), ('gip', 'GIP'), ('gmd', 'GMD'), ('gnf', 'GNF'), ('gtq', 'GTQ'), ('gyd', 'GYD'), ('hkd', 'HKD'), ('hnl', 'HNL'), ('hrk', 'HRK'), ('htg', 'HTG'), ('huf', 'HUF'), ('idr', 'IDR'), ('ils', 'ILS'), ('inr', 'INR'), ('isk', 'ISK'), ('jmd', 'JMD'), ('jpy', 'JPY'), ('kes', 'KES'), ('kgs', 'KGS'), ('khr', 'KHR'), ('kmf', 'KMF'), ('krw', 'KRW'), ('kyd', 'KYD'), ('kzt', 'KZT'), ('lak', 'LAK'), ('lbp', 'LBP'), ('lkr', 'LKR'), ('lrd', 'LRD'), ('lsl', 'LSL'), ('mad', 'MAD'), ('mdl', 'MDL'), ('mga', 'MGA'), ('mkd', 'MKD'), ('mmk', 'MMK'), ('mnt', 'MNT'), ('mop', 'MOP'), ('mro', 'MRO'), ('mur', 'MUR'), ('mvr', 'MVR'), ('mwk', 'MWK'), ('mxn', 'MXN'), ('myr', 'MYR'), ('mzn', 'MZN'), ('nad', 'NAD'), ('ngn', 'NGN'), ('nio', 'NIO'), ('nok', 'NOK'), ('npr', 'NPR'), ('nzd', 'NZD'), ('pab', 'PAB'), ('pen', 'PEN'), ('pgk', 'PGK'), ('php', 'PHP'), ('pkr', 'PKR'), ('pln', 'PLN'), ('pyg', 'PYG'), ('qar', 'QAR'), ('ron', 'RON'), ('rsd', 'RSD'), ('rub', 'RUB'), ('rwf', 'RWF'), ('sar', 'SAR'), ('sbd', 'SBD'), ('scr', 'SCR'), ('sek', 'SEK'), ('sgd', 'SGD'), ('shp', 'SHP'), ('sll', 'SLL'), ('sos', 'SOS'), ('srd', 'SRD'), ('std', 'STD'), ('svc', 'SVC'), ('szl', 'SZL'), ('thb', 'THB'), ('tjs', 'TJS'), ('top', 'TOP'), ('try', 'TRY'), ('ttd', 'TTD'), ('twd', 'TWD'), ('tzs', 'TZS'), ('uah', 'UAH'), ('ugx', 'UGX'), ('uyu', 'UYU'), ('uzs', 'UZS'), ('vnd', 'VND'), ('vuv', 'VUV'), ('wst', 'WST'), ('xaf', 'XAF'), ('xcd', 'XCD'), ('xof', 'XOF'), ('xpf', 'XPF'), ('yer', 'YER'), ('zar', 'ZAR'), ('zmw', 'ZMW')], help_text='If amount_off has been set, the three-letter ISO code for the currency of the amount to take off.', max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='stripecoupon',
            name='duration_in_months',
            field=models.PositiveIntegerField(blank=True, help_text='If duration is repeating, the number of months the coupon applies. Null if coupon duration is forever or once.', null=True),
        ),
        migrations.AlterField(
            model_name='stripecoupon',
            name='metadata',
            field=django_extensions.db.fields.json.JSONField(default=dict, help_text='Set of key/value pairs that you can attach to an object. It can be useful for storing additional information about the object in a structured format.'),
        ),
        migrations.AlterField(
            model_name='stripecoupon',
            name='percent_off',
            field=models.PositiveIntegerField(blank=True, help_text='Percent that will be taken off the subtotal of any invoicesfor this customer for the duration of the coupon. For example, a coupon with percent_off of 50 will make a $100 invoice $50 instead.', null=True),
        ),
    ]
