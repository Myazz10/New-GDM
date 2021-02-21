# Get and return the mp3_list that was stored in the session object
def get_session_mp3_list(request):
    session_mp3_list = None

    try:
        # Updating the session_mp3_list with what has been stored in the session object.
        session_mp3_list = request.session['mp3_list']
    except Exception:
        pass

    return session_mp3_list


# Get and return the mp4_list that was stored in the session object
def get_session_mp4_list(request):
    session_mp4_list = None

    try:
        # Updating the session_mp4_list with what has been stored in the session object.
        session_mp4_list = request.session['mp4_list']
    except Exception:
        pass

    return session_mp4_list


# Get and return the visitor_id dictionary that was stored in the session object
def get_session_visitor_id(request):
    visitor_id = None

    try:
        # Updating the session_mp3_list with what has been stored in the session object.
        visitor_id = request.session['visitor_id']
    except Exception:
        pass

    return visitor_id


# Create and return the visitor_id dictionary that is to be stored in the session object
def setup_user_session(session_id, session_mp3_list, session_mp4_list):
    visitor_id = {}
    downloads = {}

    downloads['mp3'] = session_mp3_list
    downloads['mp4'] = session_mp4_list

    visitor_id[session_id] = downloads

    print(f'With the setup_user_session, the visitor_id is: {visitor_id}')

    return visitor_id
