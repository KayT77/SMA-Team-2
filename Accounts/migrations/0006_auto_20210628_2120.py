# Generated by Django 3.2.4 on 2021-06-28 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_passwordreset'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='passwordreset',
            options={'ordering': ['user_id'], 'verbose_name_plural': 'Password Resets'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='status',
        ),
        migrations.AddField(
            model_name='passwordreset',
            name='expires_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='account_status',
            field=models.CharField(choices=[('Locked', 'Locked'), ('Unlocked', 'Unlocked')], default='Unlocked', max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='followers_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='follows_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='occupation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usersocial',
            name='facebook_link',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='usersocial',
            name='github_link',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='usersocial',
            name='instagram_link',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='usersocial',
            name='linkedin_link',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='usersocial',
            name='twitter_link',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
