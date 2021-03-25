from pytube import YouTube, Playlist  # pip install pytube
import os
from django.core.files import File
from .models import Video, TitleError
from .remove_characters import special_characters
from GDM.settings import BASE_DIR, DEFAULT_FILE_STORAGE, EMAIL_HOST_USER
from django.core.mail import send_mail


# This will handle the mp4 download...
def get_mp4(url):
    video_details = {}
    mp4_id = None
    special_characters_flag = False
    print('flag 1')
    email_sender('flag 1')

    try:
        video_obj = YouTube(url)
        print('flag 2')
        email_sender('flag 2')

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
        email_sender('flag 3')

        # Downloading the video object...
        video_obj.streams.get_highest_resolution().download()
        email_sender('flag 4 - Video Downloaded...')

        mp4_id, special_characters_flag = mp4_converter(video_obj.title, url)
        # print('flag 4')

    except Exception:
        video_details['invalid_url'] = 'This is not a valid YouTube url... Get a valid url please!'
        print(video_details['invalid_url'])
        print('flag 10')
        email_sender('flag 13 - In mp4 converter: Invalid Url in effect.')

    if mp4_id is not None:
        email_sender(f'flag 14 - In mp4 converter: mp4_id is not None. Therefore special_characters_flag = {special_characters_flag}')
        return video_details, mp4_id, special_characters_flag
        # print('flag 11')
    else:
        print('flag 12')
        email_sender('flag 15 - In mp4 converter: An error occurred...')
        return video_details, 'error occurred', special_characters_flag


# This will be giving additional support to the get_mp4 method above.
def mp4_converter(title, url):
    mp4_object = Video()
    created = False
    mp4_id = None
    special_characters_flag = False
    file_name = title
    print('flag 5')
    email_sender('flag 5 - In mp4 converter')

    # Updating the title to compare it with the mp4 file that exist for it in this folder...
    title = special_characters(title)
    email_sender('flag 6 - In mp4 converter: Searched title successfully.')

    mp4_file = f'{title}.mp4'

    try:
        print('flag 6')
        email_sender('flag 7 - In mp4 converter: Try Block')
        mp4_object.mp4 = File(open(mp4_file, mode='rb'))
        email_sender('flag 7.5 - In mp4 converter: File was successfully uploaded.')
        mp4_object.name = file_name
        mp4_object.save()
        email_sender('flag 8 - In mp4 converter: mp4 object saved.')
        mp4_id = mp4_object.pk
        print('flag 7')

        # Deleting the downloaded file after uploading it to cloudinary here...
        if mp4_file in os.listdir(BASE_DIR):
            os.remove(mp4_file)
            email_sender('flag 9 - In mp4 converter: Delete downloaded file.')

        created = True

    except Exception:
        email_sender('flag 10 - In mp4 converter: Exception and Invalid Url.')
        # pass

    print('FLAG BEFORE FLAG 8!')
    email_sender('flag 11 - In mp4 converter: Exit Try Block.')

    # Saving the object to the database if it was created successfully.
    if not created:
        # Now creating an object to inform administrator what to try and fix to improve the website's functionalities.
        error = TitleError()
        error.name = file_name
        email_sender('flag 11.3 - In mp4 converter: Before saving the url.')
        error.url = url
        email_sender('flag 11.5 - In mp4 converter: After saving the url.')
        error.save()
        print('flag 8')
        email_sender('flag 12 - In mp4 converter: mp4 object was not created. Therefore, Title Error occurred.')

        # Information that the object wasn't created successfully. We will use this value within the view.py to prevent
        # the programme from crashing.
        special_characters_flag = True
        print('special_characters_flag = True')


    return mp4_id, special_characters_flag


# My Production Debugger...
def email_sender(flag):
        subject = 'Get Dem Media - Debugger!'
        message = f'This is {flag}.'
        send_mail(subject, message, EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently = False)