# Generated by Django 3.1.7 on 2021-02-19 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0010_auto_20200508_1851'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Last name')),
                ('strip_id', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, help_text='User profile picture', null=True, upload_to='users/')),
                ('role', models.CharField(max_length=255)),
                ('visitReason', multiselectfield.db.fields.MultiSelectField(choices=[('Trader', 'I am a Trader.'), ('Financial Advisor', "I'm Financial Advisor."), ('Curious', "I'm Curious."), ('Other', 'Other Reason.')], max_length=38)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified At')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether this user should be treated as staff. ', verbose_name='staff')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active.Unselect this instead of deleting accounts.', verbose_name='active')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.country')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.region')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified At')),
                ('name', models.CharField(blank=True, max_length=225, null=True, verbose_name='Offer Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Plan Description')),
                ('valid', models.DateField(blank=True, help_text='Validity In Month', null=True, verbose_name='Validity')),
            ],
            options={
                'verbose_name_plural': 'Offers',
            },
        ),
        migrations.CreateModel(
            name='Plans',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified At')),
                ('name', models.CharField(blank=True, max_length=225, null=True, verbose_name='Plan Name')),
                ('price', models.PositiveIntegerField(blank=True, null=True, verbose_name='Plan Price')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Plan Description')),
            ],
            options={
                'verbose_name_plural': 'Plans',
            },
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified At')),
                ('stripe_id', models.CharField(blank=True, max_length=225, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.plans')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified At')),
                ('trial_period_start', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Trial Period Start')),
                ('trial_period_end', models.DateTimeField(blank=True, null=True, verbose_name='Trial Period End')),
                ('subscribeAfter', models.BooleanField(blank=True, null=True)),
                ('date_subscribed', models.DateTimeField(blank=True, null=True)),
                ('date_unsubscribed', models.DateTimeField(blank=True, null=True)),
                ('subscription_status', models.CharField(choices=[('Subscribed', 'Subscribed'), ('Unsubscribed', 'Unsubscribed'), ('Canceled', 'Canceled'), ('Rejected', 'Rejected')], default='Current', max_length=100)),
                ('valid_till', models.DateField(blank=True, null=True)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.offers')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.plans')),
                ('transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.transactions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Subscriptions',
            },
        ),
        migrations.CreateModel(
            name='PlansHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified At')),
                ('plan_start', models.DateTimeField(blank=True, null=True)),
                ('plan_end', models.DateTimeField(blank=True, null=True)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.subscriptions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Plans History',
            },
        ),
        migrations.CreateModel(
            name='PlanOffers',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified At')),
                ('offer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.offers', verbose_name='Offer')),
                ('plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.plans', verbose_name='Plan')),
            ],
            options={
                'verbose_name_plural': 'PlanOffers',
            },
        ),
        migrations.CreateModel(
            name='Bookmarks',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified At')),
                ('stock_id', models.CharField(blank=True, max_length=225, null=True, verbose_name='Stock Id')),
                ('category_id', models.CharField(blank=True, max_length=225, null=True, verbose_name='Category Id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'Bookmarks',
            },
        ),
    ]