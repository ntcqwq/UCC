import spotipy, os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get your Spotify API credentials from environment variables
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

# Set up the Spotify OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='user-top-read'))

def get_top_tracks(time_range):
    # Retrieve the user's top tracks
    top_tracks = sp.current_user_top_tracks(limit=10, time_range=time_range) 
    # Display the top tracks
    ans = "Your top 10 tracks:\n"
    for i, track in enumerate(top_tracks['items']):
        ans += f"{i+1}. {track['name']} by {track['artists'][0]['name']}\n"
    return ans

get_top_tracks("short_term")


