from .models import Audio, Video


# Removing the objects from the database that a specific user downloaded.
def clear_expired_session(visitor_id, obj_id):
    for session_id, session_id_items in visitor_id.items():
        for key, values in session_id_items.items():
            if key == 'mp3':
                remove_mp3_objects(values, obj_id)
            elif key == 'mp4':
                remove_mp4_objects(values, obj_id)


# Removing objects from the database if session is manually expired - MP3
def remove_mp3_objects(id_list, current_mp3_id):
    audios = Audio.objects.all()
    try:
        id_list.remove(current_mp3_id)
    except Exception:
        pass

    for audio in audios:
        if audio.pk in id_list:    # or audio.pk != current_mp3_id
            try:
                # Check the model overridden delete method to see the customization delete
                audio.delete()
            except Exception:
                pass


# Removing objects from the database if session is manually expired - MP4
def remove_mp4_objects(id_list, current_mp4_id):
    videos = Video.objects.all()
    try:
        id_list.remove(current_mp4_id)
    except Exception:
        pass

    for video in videos:
        if video.pk in id_list:   # or video.pk != current_mp4_id
            try:
                # Check the model overridden delete method to see the customization delete
                video.delete()
            except Exception:
                pass

