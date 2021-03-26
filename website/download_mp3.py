from moviepy.audio.io.AudioFileClip import AudioFileClip  # pip install moviepy
from pytube import YouTube, Playlist  # pip install pytube
import os
from django.core.files import File
from .models import Audio, TitleError
from .remove_characters import special_characters
from GDM.settings import BASE_DIR


# This will handle the mp3 download...
def get_mp3(url):
    video_details = {}
    mp3_id = None
    special_characters_flag = False

    print('flag 1')

    try:
        video = YouTube(url)

        print('flag 2')

        length = video.length
        temp_length = str(length)

        if len(str(length)) == 3:
            length = temp_length[0] + ':' + temp_length[1:]
        elif len(str(length)) == 4:
            length = temp_length[:2] + ':' + temp_length[2:]
        elif len(str(length)) == 5:
            length = temp_length[0] + ':' + \
                temp_length[1:3] + ':' + temp_length[3:]

        video_details['length'] = length
        video_details['thumbnail'] = video.thumbnail_url
        video_details['title'] = video.title
        video_details['author'] = video.author
        video_details['views'] = video.views
        video_details['publish_date'] = video.publish_date.date

        # Downloading the video object...
        video.streams.filter(only_audio=True).first().download()
        mp3_id, special_characters_flag = mp3_converter(video.title, url)

        print('flag 11')

    except Exception:
        video_details['invalid_url'] = 'This is not a valid YouTube url... Get a valid url please!'
        print(video_details['invalid_url'])

    if mp3_id is not None:
        print('flag 12')
        return video_details, mp3_id, special_characters_flag
    else:
        print('flag 13')
        return video_details, 'error occurred', special_characters_flag


# This will be giving additional support to the get_mp3 method above.
def mp3_converter(title, url):
    mp3_object = Audio()
    created = False
    mp3_id = None
    special_characters_flag = False
    file_name = title

    print('flag 3')

    print('flag 4')

    # Updating the title to compare it with the mp4 file that exist for it in this folder...
    title = special_characters(title)

    print('flag 5')

    mp3_file = f'{title}.mp3'
    mp4_file = f'{title}.mp4'

    # Converting MP4 to MP3
    clip = AudioFileClip(mp4_file)
    clip.write_audiofile(mp3_file)
    clip.close()

    print('flag 6')

    try:
        # Opening the mp3 file to create an object to store to the database.
        mp3_object.mp3 = File(open(mp3_file, mode='rb'))
        mp3_object.name = file_name
        mp3_object.save()
        mp3_id = mp3_object.pk

        print('flag 7')

        # Deleting the downloaded file after uploading it to cloudinary here...
        if mp4_file in os.listdir(BASE_DIR):
            os.remove(mp4_file)
    
        if mp3_file in os.listdir(BASE_DIR):
            os.remove(mp3_file)

        created = True

        print('flag 8')

    except Exception:
        print("MP4 file cannot open properly")

    # Saving the object to the database.
    if not created:
        # Information that the object wasn't created successfully. We will use this value within the view.py to prevent
        # the programme from crashing.
        special_characters_flag = True

        # Now creating an object to inform administrator what to try and fix to improve the website's functionalities.
        error = TitleError()
        error.name = file_name
        error.url = str(url)
        error.email_sender()
        error.save()
        print('flag 9')
    
    print('flag 10')

    return mp3_id, special_characters_flag
