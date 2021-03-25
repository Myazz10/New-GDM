from pytube import YouTube, Playlist  # pip install pytube
import os
from django.core.files import File
from .models import Video, TitleError
from .remove_characters import special_characters
from GDM.settings import BASE_DIR


# This will handle the mp4 download...
def get_mp4(url):
    video_details = {}
    mp4_id = None
    special_characters_flag = False
    print('flag 1')

    try:
        video_obj = YouTube(url)
        print('flag 2')

        length = video_obj.length
        temp_length = str(length)

        if len(str(length)) == 3:
            length = temp_length[0] + ':' + temp_length[1:]
        elif len(str(length)) == 4:
            length = temp_length[:2] + ':' + temp_length[2:]
        elif len(str(length)) == 5:
            length = temp_length[0] + ':' + \
                temp_length[1:3] + ':' + temp_length[3:]

        video_details['length'] = length
        video_details['thumbnail'] = video_obj.thumbnail_url
        video_details['title'] = video_obj.title
        video_details['author'] = video_obj.author
        video_details['views'] = video_obj.views
        video_details['publish_date'] = video_obj.publish_date.date
        print('flag 3')

        # Downloading the video object...
        video_obj.streams.get_highest_resolution().download()
        mp4_id, special_characters_flag = mp4_converter(video_obj.title, url)
        print('flag 4')

    except Exception:
        video_details['invalid_url'] = 'This is not a valid YouTube url... Get a valid url please!'
        print(video_details['invalid_url'])
        print('flag 10')

    if mp4_id is not None:
        return video_details, mp4_id, special_characters_flag
        print('flag 11')
    else:
        print('flag 12')
        return video_details, 'error occurred', special_characters_flag


# This will be giving additional support to the get_mp4 method above.
def mp4_converter(title, url):
    mp4_object = Video()
    created = False
    mp4_id = None
    special_characters_flag = False
    file_name = title
    print('flag 5')

    # Updating the title to compare it with the mp4 file that exist for it in this folder...
    title = special_characters(title)

    mp4_file = f'{title}.mp4'

    try:
        print('flag 6')
        mp4_object.mp4 = File(open(mp4_file, mode='rb'))
        mp4_object.name = file_name
        mp4_object.save()
        mp4_id = mp4_object.pk
        print('flag 7')

        # Deleting the downloaded file after uploading it to cloudinary here...
        if mp4_file in os.listdir(BASE_DIR):
            os.remove(mp4_file)

        created = True

    except Exception:
        print('flag 8')
        pass

    # Saving the object to the database if it was created successfully.
    if not created:
        # Information that the object wasn't created successfully. We will use this value within the view.py to prevent
        # the programme from crashing.
        special_characters_flag = True

        # Now creating an object to inform administrator what to try and fix to improve the website's functionalities.
        error = TitleError()
        error.name = file_name
        error.url = url
        error.save()
        print('flag 9')

    return mp4_id, special_characters_flag
