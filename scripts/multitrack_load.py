# The folder models_files/ was created through this repository:
# https://github.com/ignacio-nava/Scrapy-MTK

import pandas as pd

from django.contrib.auth.models import User

from multitracks.models import Genre, Artist, Multitrack

def getLorem():
    lorem = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    return lorem

def getArtist(df, index):
    artist, created = Artist.objects.get_or_create(name=df['name'][index])
    contact = df['contact'][index]
    if created and contact:
        artist.contact = contact
        artist.save()
    return artist

def run():
    # Open all CSV files
    df_genre = pd.read_csv('scripts/models_files/genre.csv')
    df_artist = pd.read_csv('scripts/models_files/artist.csv').fillna(False) # Replace nan values for False
    df_multitrack = pd.read_csv('scripts/models_files/multitrack.csv')

    # Delete data from models
    Genre.objects.all().delete()
    Artist.objects.all().delete()
    Multitrack.objects.all().delete()

    # Create data
    for row, data in df_multitrack.iterrows():
        g, _ = Genre.objects.get_or_create(name=df_genre['name'][data['genre']])
        a = getArtist(df_artist, data['artist'])
        u = User.objects.get(pk=1) # First superuser created
        m = Multitrack(
            title=data['title'],
            preview=data['preview'],
            number_channels=data['number_channels'],
            file_zip=data['file_zip'],
            file_size=data['file_size'],
            description=getLorem(),
            artist=a,
            genre=g,
            owner=u
        )

        m.save()