from django.shortcuts import render
from .download_mp3 import get_mp3
from .download_mp4 import get_mp4
from .comments import get_comments
from .models import Audio, Video
from datetime import datetime, time, timedelta
import pytz
from .removing_user_session import clear_expired_session
from .user_session_details import get_session_mp3_list, get_session_mp4_list, get_session_visitor_id, setup_user_session

today = datetime.now()


# Home Page Route
def home(request):
    context = {}
    result = False
    session_is_expired = False

    if request.method == 'POST':
        submission_form = request.POST.get('submission')

        print(submission_form)
        if submission_form == 'url-form':
            video_details = None
            audio = None
            video = None
            mp3_id = None
            mp4_id = None
            expiry_date = None
            session_mp3_id = None
            session_mp4_id = None
            session_mp3_list = []
            session_mp4_list = []
            invalid_url = False
            special_characters_flag = False

            session_id = request.session._get_or_create_session_key()

            session_mp3_list = get_session_mp3_list(request)
            session_mp4_list = get_session_mp4_list(request)

            # Submitted Form Data
            search_url = request.POST.get('search')
            checked_radio = request.POST.get('file-type')

            if checked_radio == 'mp3':
                video_details, mp3_id, special_characters_flag = get_mp3(
                    search_url)

                if mp3_id == 'error occurred':
                    invalid_url = True
                else:
                    audio = transporter(mp3_id, 'audio')
                    context['audio'] = audio

                    # Handling some sessions here -> Start
                    try:
                        session_mp3_id = request.session['mp3_id']

                        # Updating the session_mp3_list with what has been stored in the session object.
                        session_mp3_list = request.session['mp3_list']
                        if session_mp3_id not in session_mp3_list:
                            session_mp3_list.append(session_mp3_id)

                        # Updating the session_mp3_list with what has been stored in the session object.
                        session_mp3_list = request.session['mp3_list']
                        if session_mp3_id not in session_mp3_list:
                            session_mp3_list.append(session_mp3_id)

                        elif session_mp3_list is None:
                            session_mp3_list = []
                            session_mp3_list.append(session_mp3_id)

                    except Exception:
                        # Storing the current mp3_id in the session object to use
                        request.session['mp3_id'] = mp3_id

                    # Updating the session_mp3_list with the current mp3 object id and update the session object again.
                    try:
                        session_mp3_list.append(mp3_id)
                    except AttributeError:
                        session_mp3_list = []
                        session_mp3_list.append(session_mp3_id)
                        session_mp3_list.append(mp3_id)

                    request.session['mp3_id'] = mp3_id
                    request.session['mp3_list'] = session_mp3_list

                    try:
                        expiry_date = request.session['expiry_date']

                        # Retrieving and converting a string date variable from the session
                        expiry_date = datetime.strptime(
                            expiry_date, "%Y-%m-%d %H:%M:%S.%f")
                        expiry_date = expiry_date + timedelta(minutes=5)

                        print(f'Expiry Date: {expiry_date}')

                    except Exception:
                        # Storing a string version of the datetime object in the session
                        request.session['expiry_date'] = str(today)
                        # print('New exp date created')

                    # Current Date
                    current_date = datetime.now()

                    print(f'Today: {current_date}')

                    # replace the timezone in both time
                    if expiry_date:
                        expiry_date = expiry_date.replace(tzinfo=pytz.utc)
                        current_date = current_date.replace(tzinfo=pytz.utc)

                        if expiry_date < current_date:
                            session_is_expired = True
                            # print("Time Crossed")
                        else:
                            pass
                            # print("Time not crossed")
                    # Handling some sessions here -> End

            elif checked_radio == 'mp4':
                video_details, mp4_id, special_characters_flag = get_mp4(search_url)

                if mp4_id == 'error occurred':
                    invalid_url = True
                else:
                    video = transporter(mp4_id, 'video')
                    context['video'] = video

                    # Handling some sessions here -> Start
                    try:
                        session_mp4_id = request.session['mp4_id']

                        # Updating the session_mp4_list with what has been stored in the session object.
                        session_mp4_list = request.session['mp4_list']

                        if session_mp4_id not in session_mp4_list:
                            session_mp4_list.append(session_mp4_id)

                        elif session_mp4_list is None:
                            session_mp4_list = []
                            session_mp4_list.append(session_mp4_id)

                    except Exception:
                        # Storing the current mp4_id in the session object to use
                        request.session['mp4_id'] = mp4_id

                    # Updating the session_mp4_list with the current mp4 object id and update the session object again.
                    try:
                        session_mp4_list.append(mp4_id)
                    except AttributeError:
                        session_mp4_list = []
                        session_mp4_list.append(session_mp4_id)
                        session_mp4_list.append(mp4_id)

                    request.session['mp4_id'] = mp4_id
                    request.session['mp4_list'] = session_mp4_list

                    try:
                        expiry_date = request.session['expiry_date']

                        # Retrieving and converting a string date variable from the session
                        expiry_date = datetime.strptime(
                            expiry_date, "%Y-%m-%d %H:%M:%S.%f")
                        expiry_date = expiry_date + timedelta(minutes=5)

                        print(f'Expiry Date: {expiry_date}')

                    except Exception:
                        # Storing a string version of the datetime object in the session
                        request.session['expiry_date'] = str(today)
                        # print('New exp date created')

                    # Current Date
                    current_date = datetime.now()

                    print(f'Today: {current_date}')

                    # replace the timezone in both time
                    if expiry_date:
                        expiry_date = expiry_date.replace(tzinfo=pytz.utc)
                        current_date = current_date.replace(tzinfo=pytz.utc)

                        if expiry_date < current_date:
                            session_is_expired = True
                            # print("Time Crossed")
                        else:
                            pass
                            # print("Time not crossed")
                    # Handling some sessions here -> End

            elif checked_radio == 'mp3-playlist':
                # get_mp3_playlist(search_url)
                pass
            elif checked_radio == 'mp4-playlist':
                # get_mp4_playlist(search_url)
                pass
            else:
                pass

            """
            if checked_radio == 'mp3':
                video_details, mp3_id, special_characters_flag = mp3(search_url)

                if mp3_id == 'error occurred':
                    invalid_url = True
                else:
                    audio = transporter(mp3_id, 'audio')
                    context['audio'] = audio

            elif checked_radio == 'mp4':
                video_details, mp4_id, special_characters_flag = mp4(search_url)

                if mp4_id == 'error occurred':
                        invalid_url = True
                    else:
                        video = transporter(mp4_id, 'video')
                        context['video'] = video
            """

            if not invalid_url:
                # Setting up the user session details to reference deleting later...
                request.session['visitor_id'] = setup_user_session(
                    session_id, session_mp3_list, session_mp4_list)

                # To clean up the visitor's downloads
                if session_is_expired:
                    visitor_id = get_session_visitor_id(request)

                    if mp3_id is not None:
                        clear_expired_session(visitor_id, mp3_id)
                    elif mp4_id is not None:
                        clear_expired_session(visitor_id, mp4_id)

                    del request.session['expiry_date']

                    try:
                        del request.session['mp3_list']
                    except Exception:
                        pass

                    try:
                        del request.session['mp4_list']
                    except Exception:
                        pass

                    try:
                        del request.session['visitor_id']
                    except Exception:
                        pass

                    request.session.modified = True

                result = True
                context['title'] = video_details['title']
                context['thumbnail'] = video_details['thumbnail']
                context['author'] = video_details['author']
                context['publish_date'] = video_details['publish_date']
                context['views'] = video_details['views']
                context['length'] = video_details['length']
            else:
                if special_characters_flag:
                    context['special_characters_flag'] = 'This video url cannot be converted right now. Please try again ' \
                                                        'in 24 hours. You may also try another url now.'
                else:
                    context['invalid_url'] = video_details['invalid_url']

            # Cleaning up the session database of the expired sessions.
            #if session_is_expired:
            #    request.session.clear_expired()
        
        elif submission_form == 'comment-form':
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')

            get_comments(name, email, message)
            success_comment = f"Hi {name.title()}, thanks for the contact! We'll get back to you soon."
            context['success_comment'] = success_comment

    context['result'] = result
    context['current_year'] = today.year

    return render(request, 'website/home.html', context)


# Receiving the id number of an object and it will return the object matching the id number it received
def transporter(obj_id, file):
    if file == 'audio':
        audio = Audio.objects.get(pk=obj_id)
        return audio

    elif file == 'video':
        video = Video.objects.get(pk=obj_id)
        return video
