# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
import pyconde.attendees.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sponsorship', '__first__'),
        ('conference', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='DietaryPreference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_name', models.CharField(max_length=100, verbose_name='Company', blank=True)),
                ('first_name', models.CharField(max_length=250, verbose_name='First name')),
                ('last_name', models.CharField(max_length=250, verbose_name='Last name')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('street', models.CharField(max_length=100, verbose_name='Street and house number')),
                ('zip_code', models.CharField(max_length=20, verbose_name='Zip code')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('country', models.CharField(max_length=100, verbose_name='Country')),
                ('vat_id', models.CharField(max_length=16, verbose_name='VAT-ID', blank=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date (added)')),
                ('state', models.CharField(default='incomplete', max_length=25, verbose_name='Status', choices=[('incomplete', 'Purchase incomplete'), ('new', 'new'), ('invoice_created', 'invoice created'), ('payment_received', 'payment received'), ('canceled', 'canceled')])),
                ('comments', models.TextField(verbose_name='Comments', blank=True)),
                ('payment_method', models.CharField(default='invoice', max_length=20, verbose_name='Payment method', choices=[('invoice', 'Invoice'), ('creditcard', 'Credit card'), ('elv', 'ELV')])),
                ('payment_transaction', models.CharField(max_length=255, verbose_name='Transaction ID', blank=True)),
                ('payment_total', models.FloatField(null=True, verbose_name='Payment total', blank=True)),
                ('exported', models.BooleanField(default=False, verbose_name='Exported')),
                ('invoice_number', models.IntegerField(null=True, verbose_name='Invoice number', blank=True)),
                ('invoice_filename', models.CharField(max_length=255, null=True, verbose_name='Invoice filename', blank=True)),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='conference', to='conference.Conference', null=True)),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Purchase',
                'verbose_name_plural': 'Purchases',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date (added)')),
                ('canceled', models.BooleanField(default=False, verbose_name='Canceled')),
            ],
            options={
                'ordering': ('ticket_type__tutorial_ticket', 'ticket_type__product_number'),
            },
        ),
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_number', models.IntegerField(help_text='Will be created when you save the first time.', verbose_name='Product number', blank=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('fee', models.FloatField(default=0, verbose_name='Fee')),
                ('max_purchases', models.PositiveIntegerField(default=0, help_text='0 means no limit', verbose_name='Max. purchases')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is active')),
                ('is_on_desk_active', models.BooleanField(default=False, verbose_name='Allow on desk purchase')),
                ('date_valid_from', models.DateTimeField(verbose_name='Sale start')),
                ('date_valid_to', models.DateTimeField(verbose_name='Sale end')),
                ('valid_on', models.DateField(blank=True, null=True, verbose_name='Valid on', validators=[pyconde.attendees.validators.during_conference])),
                ('tutorial_ticket', models.BooleanField(default=False, verbose_name='Tutorial ticket')),
                ('remarks', models.TextField(verbose_name='Remarks', blank=True)),
                ('allow_editing', models.NullBooleanField(verbose_name='Allow editing')),
                ('editable_fields', models.TextField(verbose_name='Editable fields', blank=True)),
                ('editable_until', models.DateTimeField(null=True, verbose_name='Editable until', blank=True)),
                ('prevent_invoice', models.BooleanField(default=False, help_text='If checked, a purchase, that contains only tickets of ticket types where this is checked, will not be send to the user. This can be useful for e.g. sponsor tickets', verbose_name='Conditionally prevent invoice to user')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='conference', to='conference.Conference', null=True)),
                ('content_type', models.ForeignKey(verbose_name='Ticket to generate', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('tutorial_ticket', 'product_number', 'vouchertype_needed'),
                'verbose_name': 'Ticket type',
                'verbose_name_plural': 'Ticket type',
            },
        ),
        migrations.CreateModel(
            name='TShirtSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('size', models.CharField(max_length=100, verbose_name='Size')),
                ('sort', models.IntegerField(default=999, verbose_name='Sort order')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='conference', to='conference.Conference', null=True)),
            ],
            options={
                'ordering': ('sort',),
                'verbose_name': 'T-Shirt size',
                'verbose_name_plural': 'T-Shirt sizes',
            },
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text='Can be left blank, code will be created when you save.', max_length=12, verbose_name='Code', blank=True)),
                ('remarks', models.CharField(max_length=254, verbose_name='Remarks', blank=True)),
                ('date_valid', models.DateTimeField(help_text='The voucher is valid until this date', verbose_name='Date (valid)')),
                ('is_used', models.BooleanField(default=False, verbose_name='Is used')),
            ],
            options={
                'verbose_name': 'Voucher',
                'verbose_name_plural': 'Vouchers',
            },
        ),
        migrations.CreateModel(
            name='VoucherType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='voucher type')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='conference', to='conference.Conference', null=True)),
            ],
            options={
                'verbose_name': 'voucher type',
                'verbose_name_plural': 'voucher types',
            },
        ),
        migrations.CreateModel(
            name='SIMCardTicket',
            fields=[
                ('ticket_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='attendees.Ticket')),
                ('first_name', models.CharField(max_length=250, verbose_name='First name')),
                ('last_name', models.CharField(max_length=250, verbose_name='Last name')),
                ('date_of_birth', models.DateField(verbose_name='Date of birth')),
                ('gender', models.CharField(max_length=6, verbose_name='Gender', choices=[('female', 'female'), ('male', 'male')])),
                ('hotel_name', models.CharField(help_text='Name of your hotel or host for your stay.', max_length=100, verbose_name='Host', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('street', models.CharField(max_length=100, verbose_name='Street and house number of host')),
                ('zip_code', models.CharField(max_length=20, verbose_name='Zip code of host')),
                ('city', models.CharField(max_length=100, verbose_name='City of host')),
                ('country', models.CharField(max_length=100, verbose_name='Country of host')),
                ('phone', models.CharField(help_text='Please supply the phone number of your hotel or host.', max_length=100, verbose_name='Host phone number')),
                ('sim_id', models.CharField(help_text='The IMSI of the SIM Card associated with this account.', max_length=20, verbose_name='IMSI', blank=True)),
            ],
            options={
                'verbose_name': 'SIM Card',
                'verbose_name_plural': 'SIM Cards',
            },
            bases=('attendees.ticket',),
        ),
        migrations.CreateModel(
            name='SupportTicket',
            fields=[
                ('ticket_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='attendees.Ticket')),
            ],
            options={
                'verbose_name': 'Support Ticket',
                'verbose_name_plural': 'Support Tickets',
            },
            bases=('attendees.ticket',),
        ),
        migrations.CreateModel(
            name='VenueTicket',
            fields=[
                ('ticket_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='attendees.Ticket')),
                ('first_name', models.CharField(max_length=250, verbose_name='First name', blank=True)),
                ('last_name', models.CharField(max_length=250, verbose_name='Last name', blank=True)),
                ('organisation', models.CharField(max_length=100, verbose_name='Organization', blank=True)),
                ('dietary_preferences', models.ManyToManyField(to='attendees.DietaryPreference', verbose_name='Dietary preferences', blank=True)),
                ('shirtsize', models.ForeignKey(verbose_name='Desired T-Shirt size', blank=True, to='attendees.TShirtSize', null=True)),
                ('sponsor', models.ForeignKey(verbose_name='Sponsor', blank=True, to='sponsorship.Sponsor', null=True)),
            ],
            options={
                'verbose_name': 'Conference Ticket',
                'verbose_name_plural': 'Conference Tickets',
            },
            bases=('attendees.ticket',),
        ),
        migrations.AddField(
            model_name='voucher',
            name='type',
            field=models.ForeignKey(verbose_name='voucher type', to='attendees.VoucherType', null=True),
        ),
        migrations.AddField(
            model_name='tickettype',
            name='vouchertype_needed',
            field=models.ForeignKey(verbose_name='voucher type needed', blank=True, to='attendees.VoucherType', null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='purchase',
            field=models.ForeignKey(to='attendees.Purchase'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_type',
            field=models.ForeignKey(verbose_name='Ticket type', to='attendees.TicketType'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(related_name='attendees_ticket_tickets', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='venueticket',
            name='voucher',
            field=models.ForeignKey(verbose_name='Voucher', blank=True, to='attendees.Voucher', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='tickettype',
            unique_together=set([('product_number', 'conference')]),
        ),
    ]
