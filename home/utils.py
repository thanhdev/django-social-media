import re


def get_youtube_thumbnail(url):
    video_id_pattern = re.compile(
        r'(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|v\/))([^?&"\'<>#\s]{11})'  # noqa
    )
    match = video_id_pattern.search(url)

    if match:
        video_id = match.group(1)
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"
        return thumbnail_url
    else:
        return None
