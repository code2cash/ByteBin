import random
import string
import mimetypes

def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(7))

def get_file_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type:
        return mime_type.split('/')[0]
    return None
