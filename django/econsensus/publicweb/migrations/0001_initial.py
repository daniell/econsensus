# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Decision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(verbose_name='Description')),
                ('decided_date', models.DateField(null=True, verbose_name='Decided Date', blank=True)),
                ('effective_date', models.DateField(null=True, verbose_name='Effective Date', blank=True)),
                ('review_date', models.DateField(null=True, verbose_name='Review Date', blank=True)),
                ('expiry_date', models.DateField(null=True, verbose_name='Expiry Date', blank=True)),
                ('deadline', models.DateField(null=True, verbose_name='Deadline', blank=True)),
                ('archived_date', models.DateField(null=True, verbose_name='Archived Date', blank=True)),
                ('budget', models.CharField(max_length=255, verbose_name='Budget/Resources', blank=True)),
                ('people', models.CharField(max_length=255, null=True, blank=True)),
                ('meeting_people', models.CharField(max_length=255, null=True, blank=True)),
                ('status', models.CharField(default=b'proposal', max_length=10, choices=[(b'discussion', 'discussion'), (b'proposal', 'proposal'), (b'decision', 'decision'), (b'archived', 'archived')])),
                ('tags', tagging.fields.TagField(help_text=b'Enter a list of tags separated by spaces.', max_length=255, null=True, blank=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True, verbose_name='Last Modified', null=True)),
                ('last_status', models.CharField(default=b'new', max_length=10, editable=False, choices=[(b'discussion', 'discussion'), (b'proposal', 'proposal'), (b'decision', 'decision'), (b'archived', 'archived')])),
                ('excerpt', models.CharField(max_length=255, verbose_name='Excerpt', blank=True)),
                ('creation', models.DateField(auto_now_add=True, verbose_name='Creation', null=True)),
                ('author', models.ForeignKey(related_name='publicweb_decision_authored', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('editor', models.ForeignKey(related_name='publicweb_decision_edited', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('organization', models.ForeignKey(to='organizations.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('resolved', models.BooleanField(verbose_name='Resolved')),
                ('rating', models.IntegerField(default=4, choices=[(0, b'question'), (1, b'danger'), (2, b'concerns'), (3, b'consent'), (4, b'comment')])),
                ('author', models.ForeignKey(related_name='publicweb_feedback_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('decision', models.ForeignKey(verbose_name='Decision', to='publicweb.Decision')),
                ('editor', models.ForeignKey(related_name='publicweb_feedback_edited', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NotificationSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notification_level', models.IntegerField(default=1, help_text='Levels are cumulative, so if, for example, you choose to get notifications of replies to feedback, you will get notifications of all changes to main items as well.', verbose_name='Notification level', choices=[(0, '1. Silent'), (1, '2. Major events'), (2, '3. Feedback and changes'), (3, '4. Full discussion'), (4, '5. Everything, even minor changes')])),
                ('organization', models.ForeignKey(to='organizations.Organization')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganizationSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default_notification_level', models.IntegerField(help_text='Levels are cumulative, so if, for example, you choose to get notifications of replies to feedback, you will get notifications of all changes to main items as well.', choices=[(0, '1. Silent'), (1, '2. Major events'), (2, '3. Feedback and changes'), (3, '4. Full discussion'), (4, '5. Everything, even minor changes')])),
                ('organization', models.OneToOneField(to='organizations.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='notificationsettings',
            unique_together=set([('user', 'organization')]),
        ),
    ]
