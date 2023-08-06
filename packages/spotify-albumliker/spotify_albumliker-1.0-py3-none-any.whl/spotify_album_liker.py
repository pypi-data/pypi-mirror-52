import click
import sys
import spotipy
import spotipy.util as util

scope = 'user-library-modify user-library-read'


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def iterate_results_for_ids(sp, more_results, result_type=None):
    all_ids = []
    while more_results:
        if not result_type:
            all_ids += [result['id'] for result in more_results['items']]
        else:
            all_ids += [result[result_type]['id'] for result in more_results['items']]
        more_results = sp.next(more_results)
    return all_ids


def get_songs_for_album(sp, album_id):
    more_results = sp.album_tracks(album_id)
    return iterate_results_for_ids(sp, more_results)


def get_followed_albums(sp):
    more_results = sp.current_user_saved_albums()
    return iterate_results_for_ids(sp, more_results, 'album')


def find_and_save_followed_albums(sp):
    print("finding liked albums...")
    all_album_ids = get_followed_albums(sp)
    song_count = 0
    print('finding songs from liked albums...')
    for aid in all_album_ids:
        song_ids = get_songs_for_album(sp, aid)
        song_count += len(song_ids)
        for song_list in divide_chunks(song_ids, 50):
            sp.current_user_saved_tracks_add(song_list)
    print("{} songs found from {} followed albums saved".format(song_count, len(all_album_ids)))


@click.command()
@click.argument('username')
@click.option('--client_id', help="Spotify client id for your authorization app")
@click.option('--client_secret', help='Spotify client secret for your authorization app')
@click.option('--redirect_uri', help="Redirect uri you've set for your app")
def cli(username, client_id, client_secret, redirect_uri):
    token = util.prompt_for_user_token(username, scope, client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri=redirect_uri)
    if token:
        sp = spotipy.Spotify(auth=token)
        find_and_save_followed_albums(sp)
    else:
        print("Can't get token for", username)


