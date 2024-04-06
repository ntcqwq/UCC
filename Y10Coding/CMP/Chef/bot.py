import discord, os, random, spotipy, urllib.parse, asyncio, datetime, json, lyricsgenius, re
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()
client = discord.Client(intents=intents)

load_dotenv()
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
api_token = os.getenv('GENIUS_ACCESS_TOKEN')
file_path = os.getenv('FILE_PATH')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-read-recently-played"))
bot = commands.Bot(command_prefix='cook ', intents=intents)

def load_user_scores():
    with open(file_path, "r") as file:
        return json.load(file)

# Function to save user scores to JSON file
def save_user_scores(user_scores):
    with open(file_path, "w") as file:
        json.dump(user_scores, file)

@bot.event
async def on_ready():
    print(f'Successful! Logged in as {bot.user.name}')

@bot.command()
# greet command
async def greet(ctx):
    greetings = [
        ("Hello", "English"),
        ("Hola", "Spanish"),
        ("Bonjour", "French"),
        ("Hallo", "German"),
        ("Ciao", "Italian"),
        ("Привет", "Russian"),
        ("こんにちは", "Japanese"),
        ("你好", "Chinese"),
        ("안녕하세요", "Korean"),
        ("Merhaba", "Turkish"),
        ("Salam", "Arabic"),
        ("नमस्ते", "Hindi"),
        ("Shalom", "Hebrew"),
        ("Olá", "Portuguese"),
        ("Zdravstvuyte", "Russian"),
        ("Sawubona", "Zulu"),
        ("Jambo", "Swahili"),
        ("Hej", "Swedish"),
        ("Hei", "Finnish"),
        ("Szia", "Hungarian"),
        ("Goddag", "Danish"),
        ("Halló", "Icelandic"),
        ("Kumusta", "Filipino"),
        ("Sawasdee", "Thai"),
        ("Xin chào", "Vietnamese"),
        ("Selamat siang", "Indonesian"),
        ("Namaskar", "Nepali"),
        ("Tere", "Estonian"),
        ("Sveiki", "Latvian"),
        ("Labas", "Lithuanian"),
        ("Barev", "Armenian"),
        ("Salam", "Persian"),
        ("Yassas", "Greek"),
        ("Dobry den", "Czech"),
        ("Szervusz", "Hungarian"),
        ("Buna", "Romanian"),
        ("Zdravo", "Serbian"),
        ("Pryvit", "Ukrainian"),
        ("Sveikas", "Lithuanian"),
    ]
    msg = random.choice(greetings)
    await ctx.send(f"## {msg[0]}! ({msg[1]})")

@bot.command()
async def luckynumber(ctx):
    name = ctx.author.name
    number = random.randint(1, 100)
    await ctx.send(f"Hi **{name}**! Your lucky number today is: **{number}**")

@bot.command()
async def cmds(ctx):
    commands_list = [
        'cook cmds - Lists all available commands',
        'cook greet - Greet you with a random language',
        'cook luckynumber - Tells you a random lucky number',
        'cook info - Provides info about the bot',
    ]
    await ctx.send('You can use the following commands: \n' + '\n'.join(commands_list))

@bot.command()
async def info(ctx):
    await ctx.send('spotify chef bot made by @zeendabean24 and @ntcie :p')

@bot.command()
async def test(ctx):
    channel = ctx.message.channel
    embed = discord.Embed(
        title = 'Title',
        description = 'This is description.',
        colour = discord.Colour.blue()
    )

    embed.set_footer(text='This is a footer')
    embed.set_image(url='https://archive.org/download/discordprofilepictures//discordblue.png')
    embed.set_thumbnail(url='https://archive.org/download/discordprofilepictures//discordblue.png')
    embed.set_author(name='bozo', icon_url='https://archive.org/download/discordprofilepictures//discordblue.png')
    embed.add_field(name='Field Name', value='Field Value', inline=False)
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    embed.add_field(name=channel, value='Field Value', inline=True)
    
    await ctx.send(channel, embed=embed)

@bot.command()
async def recent(ctx):
    # Get the user's recently played tracks
    results = sp.current_user_recently_played(limit=1)
    # Check if there are any recently played tracks
    if results["items"]:
        item = results["items"][0]
        track_info = item['track']
        
        # Get artists' names
        artists = ', '.join([artist['name'] for artist in track_info['artists']])
        song_name = track_info['name']
        
        # Check if the track is part of a playlist
        if item["context"] and item["context"]["type"] == "playlist":
            # If the most recent item is a playlist, display the playlist information
            playlist_info = sp.playlist(item["context"]["uri"])
            embed = discord.Embed(
                title="Most Recent Song",
                description=f"**{song_name}** by {artists}",
                color=discord.Color.blue()
            )
            embed.add_field(name="Playlist", value=f"[{playlist_info['name']}]({playlist_info['external_urls']['spotify']})", inline=False)
            if playlist_info['images']:
                embed.set_thumbnail(url=playlist_info['images'][0]['url'])
        else:
            # If the most recent item is not a playlist, display the album information
            album_info = sp.album(track_info['album']['external_urls']['spotify'])
            embed = discord.Embed(
                title="Most Recent Song",
                description=f"**{song_name}** by {artists}",
                color=discord.Color.blue()
            )
            embed.add_field(name="Album", value=f"[{album_info['name']}]({album_info['external_urls']['spotify']})", inline=False)
            if album_info['images']:
                embed.set_thumbnail(url=album_info['images'][0]['url'])
        
        await ctx.send(embed=embed)
    else:
        await ctx.send("No recently played tracks found.")

async def fetch_all_playlist_tracks(playlist_id):
    tracks = []
    offset = 0
    while True:
        # Fetch a page of tracks
        response = await asyncio.to_thread(sp.playlist_tracks, playlist_id, limit=100, offset=offset)
        tracks.extend(response['items'])
        # If this page is less than the maximum limit, we've reached the end
        if len(response['items']) < 100: break
        # Prepare to fetch the next page
        offset += 100
    return tracks

class GenreSelect(discord.ui.Select):
    def __init__(self, playlists, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playlists = playlists  # Store playlists for use in the class
        # Setup options based on the playlists provided
        self.options = [discord.SelectOption(label=playlist['name'], value=playlist['id']) for playlist in playlists]
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        playlist_id = self.values[0]  # The selected playlist ID
        tracks = await fetch_all_playlist_tracks(playlist_id)
        total_tracks = len(tracks) # Basic playlist information
        # Assuming each track has a duration_ms attribute, sum them up and convert to hours, minutes, and seconds
        total_duration_ms = sum(track['track']['duration_ms'] for track in tracks if track['track'])
        total_seconds = total_duration_ms//1000
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        # Initialize a dictionary to count genres
        genre_count = {}

        # Initialize a cache for artist genres
        artist_genres_cache = {}

        async def get_artist_genres(artist_id):
            if artist_id not in artist_genres_cache:
                artist_info = await asyncio.to_thread(sp.artist, artist_id)
                artist_genres_cache[artist_id] = artist_info['genres']
            return artist_genres_cache[artist_id]

        for track in tracks:
            track_genres = set()  # A set to store unique genres for this track
            artists = track['track']['artists']
            for artist in artists:
                genres = await get_artist_genres(artist['id'])
                track_genres.update(genres)  # Add genres to the set, duplicates are automatically handled
            # Now update the genre counts based on this track's unique genres
            for genre in track_genres:
                genre_count[genre] = genre_count.get(genre, 0) + 1

        # Sort genres by frequency and select the top 10
        sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)[:10]

        # Prepare the messages
        basic_info_message = f"**Playlist Overview:**\nTotal Tracks: {total_tracks}\nTotal Duration: {hours}h {minutes}m {seconds}s\n"
        genres_message = "\n".join([f"{i+1}. {genre[0]} - {genre[1]} songs" for i, genre in enumerate(sorted_genres)])
        # Combine messages
        overview_message = basic_info_message + "**Top Genres:**\n" + genres_message
        # Send the follow-up message with the results
        await interaction.followup.send(overview_message)

class ArtistSelect(discord.ui.Select):
    def __init__(self, playlists, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playlists = playlists  # Store playlists for use in the class
        # Setup options based on the playlists provided
        self.options = [discord.SelectOption(label=playlist['name'], value=playlist['id']) for playlist in playlists]
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        playlist_id = self.values[0]  # The selected playlist ID
        tracks = await fetch_all_playlist_tracks(playlist_id)
        total_tracks = len(tracks) # Basic playlist information
        # Assuming each track has a duration_ms attribute, sum them up and convert to hours, minutes, and seconds
        total_duration_ms = sum(track['track']['duration_ms'] for track in tracks if track['track'])
        total_seconds = total_duration_ms//1000
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        artist_plays = defaultdict(int)
        artist_total_popularity = defaultdict(int)
        id_to_name = defaultdict(str)
        for track in tracks:
            for i in track['track']['artists']:
                artist_id = i['id']
                artist_name = i['name']
                track_popularity = track['track']['popularity']
                artist_plays[artist_id] += 1
                id_to_name[artist_id] = artist_name
                artist_total_popularity[artist_id] += track_popularity
        ac = sorted(list(artist_plays.items()), key=lambda x: x[1], reverse=True)
        msg = "**Top 10 Artists by Track count in playlist**"
        p = 1
        for artist, play_count in ac[:10]:
            msg += f"\n**{p}. [{id_to_name[artist]}](https://open.spotify.com/artist/{artist})** - {play_count} tracks **|** {artist_total_popularity[artist]//play_count} popularity"
            p += 1
        await interaction.followup.send(msg)

class GenreView(discord.ui.View):
    def __init__(self, playlists, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Correctly pass the playlists parameter to PlaylistSelect
        self.add_item(GenreSelect(playlists=playlists, placeholder="Choose a playlist", options=[
            discord.SelectOption(label=playlist['name'], value=playlist['id']) for playlist in playlists
        ]))

class ArtistView(discord.ui.View):
    def __init__(self, playlists, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Correctly pass the playlists parameter to PlaylistSelect
        self.add_item(ArtistSelect(playlists=playlists, placeholder="Choose a playlist", options=[
            discord.SelectOption(label=playlist['name'], value=playlist['id']) for playlist in playlists
        ]))
        
@bot.command()
async def playlist_genre(ctx):
    current_user = sp.current_user()
    uid = current_user['id'] 
    playlists = sp.current_user_playlists(limit=50)['items']  # Increase limit if necessary
    own_playlists = [playlist for playlist in playlists if playlist['owner']['id'] == uid]  # Filter for user's own playlists
    if not own_playlists:
        await ctx.send("You don't have any playlists.")
        return
    await ctx.send("Select one of your playlists:", view=GenreView(playlists=own_playlists))

@bot.command()
async def playlist_artist(ctx):
    current_user = sp.current_user()
    uid = current_user['id'] 
    playlists = sp.current_user_playlists(limit=50)['items']  # Increase limit if necessary
    own_playlists = [playlist for playlist in playlists if playlist['owner']['id'] == uid]  # Filter for user's own playlists
    if not own_playlists:
        await ctx.send("You don't have any playlists.")
        return
    await ctx.send("Select one of your playlists:", view=ArtistView(playlists=own_playlists))

@bot.command
async def fetch_all_playlist_tracks_async(playlist_id):
    tracks = []
    offset = 0
    while True:
        response = await asyncio.to_thread(sp.playlist_tracks, playlist_id, offset=offset, fields="items.track.id,total,next")
        tracks.extend(response['items'])
        if response['next'] is None:
            break
        offset = len(tracks)
    return [track['track']['id'] for track in tracks if track['track']]

@bot.command()
async def lyric_guess(ctx):
    current_user = sp.current_user()
    uid = current_user['id'] 
    playlists = sp.current_user_playlists(limit=50)['items']  # Increase limit if necessary
    own_playlists = [playlist for playlist in playlists if playlist['owner']['id'] == uid]  # Filter for user's own playlists
    if not own_playlists:
        await ctx.send("u don't have any public playlists :(")
        return
    all_tracks = []
    for playlist in own_playlists:
        tracks = await fetch_all_playlist_tracks(playlist['id'])
        all_tracks.extend(tracks)
    random_track = random.choice(all_tracks)
    genius = lyricsgenius.Genius(api_token)
    track_name = re.sub(r"\[.*?\]|\(.*?\)", "", random_track['track']['name']).strip()
    song = genius.search_song(track_name, random_track['track']['artists'][0]['name'])
    if not song:
        await ctx.send(f"Could not fetch the lyrics of the song **{track_name}** by **{random_track['track']['artists'][0]['name']}** :( please reroll command")
        return
    lyrics = song.lyrics.split('\n')
    line_counts = {}
    for line in lyrics[1:][:-1]:
        if line.strip():
            if not '[' in line and not ']' in line and not '(' in line and not ')' in line:
                if track_name in line:
                    line_counts[line] = line_counts.get(line, 0) + 2
                else:
                    line_counts[line] = line_counts.get(line, 0) + 1
    best_line = max(line_counts, key=line_counts.get)
    await ctx.send(f"**Guess the song name and artist of this verse!**\nType your guess in this format: `[Song name] | [Artist]`!\n\n>>> ## {best_line}")
    user = 0
    uid = 0
    username = 0
    try:
        user_guess = await bot.wait_for('message')
        user = user_guess.author
        uid = user.id
        username = user.name
    except asyncio.TimeoutError:
        await ctx.send(f"womp womp time's up. The correct answer is **{random_track['track']['name']}** by **{random_track['track']['artists'][0]['name']}**.")
        return
    if user_guess.content.lower().replace(' ', '').split('|') == [track_name.replace(' ', '').lower(), random_track['track']['artists'][0]['name'].replace(' ', '').lower()]:
        user_scores = load_user_scores()
        uid = str(uid)
        if not uid in user_scores.keys():
            user_scores[uid] = {
                "username": username,
                "pp": 1,
            }
        else:
            user_scores[uid]['pp'] += 1
        save_user_scores(user_scores)
        await ctx.send(f"GG **{username}**! Your guess is correct. You get **1** coin. You currently have **{user_scores[uid]['pp']}** coins.")
    else:
        await ctx.send(f"womp womp you are incorrect. The correct answer is **{random_track['track']['name']}** by **{random_track['track']['artists'][0]['name']}**.")

@bot.command()
async def blend(ctx):
    current_user = sp.current_user()
    uid = current_user['id'] 
    playlists = sp.current_user_playlists(limit=50)['items']  # Increase limit if necessary
    own_playlists = [playlist for playlist in playlists if playlist['owner']['id'] == uid]  # Filter for user's own playlists
    # Check if the user has any playlists
    if not own_playlists:
        await ctx.send("u don't have any public playlists :(")
        return
    # Fetching all tracks from all of the user's playlists
    all_tracks = []
    for playlist in own_playlists:
        tracks = await fetch_all_playlist_tracks(playlist['id'])
        all_tracks.extend(tracks)
    msg = "**Your 50-track blend:**\n>>> "
    for i in range(1, 51):
        track = random.choice(all_tracks)
        msg += f"{i}. **{track['track']['name']}** by **{track['track']['artists'][0]['name']}**\n"
        all_tracks.remove(track)
    msg += "(More features coming soon!)"
    await ctx.send(msg)

@bot.command()
async def leaderboard(ctx):
    user_scores = load_user_scores()
    scores = []
    msg = "**Top 10 users, by coins**"
    for uid in user_scores:
        scores.append([user_scores[uid]["pp"], user_scores[uid]["username"]])
    scores.sort(reverse=True)
    for i in range(min(10, len(scores))):
        msg += f"\n{i+1}. **{scores[i][1]}**: {scores[i][0]} coins"
    await ctx.send(msg)

bot.run(os.getenv("TOKEN"))