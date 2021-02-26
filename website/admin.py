from django.contrib import admin
from .models import Audio, Video, AnimatedHeaderText, WebsiteName, AudioPlaylist, VideoPlaylist,\
    PermitPlaylistDownload, MyazzDesignzProfile, TitleError, ErrorCharacter, Notice, Comment


admin.site.register(Audio)
admin.site.register(Video)
admin.site.register(AudioPlaylist)
admin.site.register(VideoPlaylist)
admin.site.site_header = 'GDM Tech Admin Dashboard'
admin.site.site_title = 'Home - GDM Tech'

MAX_OBJECTS = 1
WEBSITE_NOTICE_OBJECTS = 2


@admin.register(AnimatedHeaderText)
class AnimatedHeaderTextAdmin(admin.ModelAdmin):
    fields = ['first_paragraph', 'second_paragraph',
              'third_paragraph', 'fourth_paragraph']

    # To allow the user to only add one object for this model...
    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)


@admin.register(WebsiteName)
class WebsiteNameAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']

    # To allow the user to only add one object for this model...
    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)


@admin.register(MyazzDesignzProfile)
class MyazzDesignzProfileAdmin(admin.ModelAdmin):
    fields = ['website', 'facebook', 'twitter', 'instagram', 'pinterest']

    # To allow the user to only add one object for this model...
    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)


@admin.register(PermitPlaylistDownload)
class PermitPlaylistDownloadAdmin(admin.ModelAdmin):
    fields = ['user', 'approved']
    list_display = ['user', 'approved']

    # To allow the user to only add one object for this model...
    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)


@admin.register(TitleError)
class TitleErrorAdmin(admin.ModelAdmin):
    fields = ['name', 'error_date']
    list_display = ['name', 'error_date']


@admin.register(ErrorCharacter)
class ErrorCharacterAdmin(admin.ModelAdmin):
    fields = ['name', 'created']
    list_display = ['name', 'created']

    # To allow the user to only add one object for this model...
    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'when', 'approved']
    list_display = ['name', 'when', 'user', 'approved']

    # To allow the user to only add one object for this model...
    def has_add_permission(self, request):
        if self.model.objects.count() >= WEBSITE_NOTICE_OBJECTS:
            return False
        return super().has_add_permission(request)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ['name', 'email', 'message', 'subject', 'reply', 'replied']
    search_fields = ['name', 'email', 'replied']
    list_filter = ['name', 'email', 'date_commented', 'replied']
    list_display = ['name', 'email', 'date_commented', 'replied', 'date_replied']
    list_per_page = 30
