"""
.. module:: model
   :platform: Unix, Windows
   :synopsis: Permission

"""
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone


def file_upload_path(instance, filename):
    return 'file_{}_{}'.format(str(datetime.now().timestamp()), filename)


### Mixins ###

class AnnotationMixin(models.Model):
    """
    Each model that contains `Annotation`s must use this mixin.
    """
    annotations = GenericRelation('Annotation')

    class Meta:
        abstract = True


class CommentMixin(models.Model):
    """
    Each model that contains `Comment`s must use this mixin.
    """
    comments = GenericRelation('Comment')

    class Meta:
        abstract = True


class FollowMixin(models.Model):
    """
    Each model that can be followed by a user must use this mixin.
    """
    followers = GenericRelation('FollowStatus')
    follower_count = models.IntegerField(default=0)

    class Meta:
        abstract = True


class OwnerMixin(models.Model):
    """
    Each model that belongs to a `User` must use this mixin.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_set', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class TagMixin(models.Model):
    """
    Each model that contains `Tag`s must use this mixin.
    """
    tags = models.ManyToManyField('Tag', related_name='%(class)s_set', blank=True)

    class Meta:
        abstract = True


class VoteMixin(models.Model):
    """
    Each model that can be voted by a user must use this mixin.
    """
    votes = GenericRelation('VoteStatus')
    vote_count = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def update_vote_count(self, vote_value, voted_before):
        if voted_before:
            vote_value = vote_value * 2
        self.vote_count = self.vote_count + vote_value
        self.save()


class GenericModelMixin(models.Model):
    """
    Allows generic relations between different models.
    See https://docs.djangoproject.com/en/2.1/ref/contrib/contenttypes/
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


### Models ###

## User & Related Models

class User(AbstractUser, AnnotationMixin, CommentMixin, FollowMixin, TagMixin, VoteMixin):
   
   # Related fields
    blocked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False,
                                           related_name='user_blocked_users')

    # Own fields
    profile_photo = models.FileField(upload_to=file_upload_path, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    """
    Corporate users have their profiles having their corporate data.
    Since it's not feasible to create different tables for both
    or to use abstract tables and user groups doesn't meet the requirements
    due to extra fields in the db, creating another profile is preferred.
    """
    is_corporate_user = models.BooleanField(default=False)
    corporate_profile = models.OneToOneField('CorporateUserProfile', on_delete=models.SET_NULL,
                                             null=True, default=None)

    class Meta:
        unique_together = (('email',), ('username',))


class CorporateUserProfile(models.Model):
    url = models.URLField(max_length=200, null=True, blank=True)


## Event & Related Models

class Event(AnnotationMixin, CommentMixin, FollowMixin, OwnerMixin, TagMixin, VoteMixin):
    """
    :class:`FollowStatus` uses owner mixin and GenericModel Mixin.
    .. note:: 
       Related fields: artists, location
    .. note::
        Own fiels: featured_image, title, description, date, price, organizer_url, created, updated
    """
    # Related fields
    # TODO Decide if an artist must be a User in our system.
    artists = models.ManyToManyField(settings.AUTH_USER_MODEL, db_table='event_artists',
                                     related_name='performed_events', blank=True)
    location = models.OneToOneField('Location', on_delete=models.SET_NULL, default=None, null=True)

    # Own fields
    featured_image = models.FileField(upload_to=file_upload_path, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, default=0.0)
    organizer_url = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Annotation(GenericModelMixin, OwnerMixin):
    data = JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class AttendanceStatus(OwnerMixin):
    """
    :class:`AttendanceStatus` uses owner mixin.
    .. note:: 
       There can be only one attendance status between User and Event.
    """
    ATTENDANCE_STATUS = (
        ('Y', 'Yes'),
        ('N', 'No'),
        ('M', 'Maybe'),
        ('A', 'Attended'),
        ('B', 'Blocked'),
    )
    event = models.ForeignKey(Event, related_name='attendance_status', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=ATTENDANCE_STATUS)

    class Meta:    
        # There can be only one attendance status between User and Event.     
        unique_together = ('owner', 'event')


class Comment(GenericModelMixin, OwnerMixin):
    """
    :class:`Comment` uses owner mixin and GenericModel Mixin. It has content(string), created and updated(datetime) properties.
    """
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Conversation(OwnerMixin):
    """
    :class:`Conversation` uses owner mixin and it participant, created and updated properties.
    """
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='participated_conversation_set',
                                    on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class FollowStatus(GenericModelMixin, OwnerMixin):
    """
    :class:`FollowStatus` uses owner mixin and GenericModel Mixin.
    .. note:: 
       A user cannot follow the same item more than once
    """
    class Meta:  
        # A user cannot follow the same item more than once
        unique_together = ('owner', 'content_type', 'object_id')


class Location(models.Model):
    city = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    google_place_id = models.CharField(max_length=100)
    name = models.CharField(max_length=250)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)


class Media(OwnerMixin):
    file = models.FileField(upload_to=file_upload_path)
    event = models.ForeignKey(Event, related_name='medias', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Message(OwnerMixin):
    """
    :class:`Message` uses owner mixin.
    .. note:: 
        Related fields : receiver, conversation
    .. note::
        Own fields: content, created    
    """
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_message_set',
                                 on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)

    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class ShareStatus(OwnerMixin):
    """
    :class:`ShareStatus` uses owner mixin.
    .. note:: 
        There can be only one share status between User and Event.
    """
    event = models.ForeignKey(Event, related_name='share_status', on_delete=models.CASCADE)

    class Meta:
        # 
        unique_together = ('owner', 'event')


class Tag(models.Model):
    """
    :class:`Tag` has only name property.
    """
    name = models.CharField(max_length=20)


class VoteStatus(GenericModelMixin, OwnerMixin):
    """
    :class:`VoteStatus` uses owner mixin and GenericModelMixin
    .. note:: 
        A user cannot vote for the same item more than once
    """
    VOTE_CHOICES = (
        ('U', 'Up'),
        ('D', 'Down'),
    )
    vote = models.CharField(max_length=1, choices=VOTE_CHOICES)

    class Meta:
        # A user cannot vote for the same item more than once
        unique_together = ('owner', 'content_type', 'object_id')

    @property
    def vote_value(self):
        vote_value = 0
        if self.vote == 'U':
            vote_value = 1
        elif self.vote == 'D':
            vote_value = -1
        return  vote_value
