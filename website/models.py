import os
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary_storage.validators import validate_video
from GDM.settings import DEFAULT_FILE_STORAGE


class AnimatedHeaderText(models.Model):
    first_paragraph = models.CharField(max_length=50, null=True, blank=True)
    second_paragraph = models.CharField(max_length=50, null=True, blank=True)
    third_paragraph = models.CharField(max_length=50, null=True, blank=True)
    fourth_paragraph = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'Animated Header Text'


class WebsiteName(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)


class Audio(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    mp3 = models.FileField(upload_to='audios/', null=True, blank=True, storage=VideoMediaCloudinaryStorage(), validators=[validate_video])

    def __str__(self):
        return f'{self.name}'


class Video(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    mp4 = models.FileField(upload_to='videos/', null=True, blank=True, storage=VideoMediaCloudinaryStorage(), validators=[validate_video])

    def __str__(self):
        return f'{self.name}'


class AudioPlaylist(models.Model):
    mp3 = models.FileField(upload_to='audios/', null=True, blank=True)


class VideoPlaylist(models.Model):
    mp4 = models.FileField(upload_to='videos/', null=True, blank=True)


class PermitPlaylistDownload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Approved by {self.user.username.title()}'


class MyazzDesignzProfile(models.Model):
    website = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    pinterest = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'Myazz Designz Contacts'


class TitleError(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    error_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}'


class ErrorCharacter(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}'


class Notice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    when = models.DateTimeField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name.title()}'


class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f'{self.name.title()}'

# To clear the potential problems with the titles that contains special characters that will throw an error
def special_characters(title):
    error_characters = ErrorCharacter.objects.all()

    if not error_characters.exists():
        error_characters = ['"', '.', '$', ',', '#', "'", '\\', '/']

        for character in title:
            if character in error_characters:
                title = title.replace(character, "")

        # Converting the list to a string to save it to the database
        error_characters = ", ".join(error_characters)

        errors = ErrorCharacter()
        errors.name = error_characters
        errors.save()
    else:
        # Converting the string back to a list to loop over it...
        errors_list = list(error_characters.first().name.split(", "))
        for character in title:
            if character in errors_list:
                title = title.replace(character, "")

    return title

