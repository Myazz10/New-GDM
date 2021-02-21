from .models import ErrorCharacter


# To clear the potential problems with the titles that contains special characters that will throw an error
def special_characters(title):
    print('Within the special characters section - start')
    error_characters = ErrorCharacter.objects.all()

    print(title)
    if not error_characters.exists():
        error_characters = ['"', '.', '$', ',', '#', "'", '\\', '/']
        # spaces = ["  ", "   ", "    "]

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

    print(title)

    print('Within the special characters section - end')
    return title
