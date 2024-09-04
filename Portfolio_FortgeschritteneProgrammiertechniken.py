"""
Portfolioarbeit Semester 2, Fortgeschrittene Programmiertechniken
author: Quirin Barth

Did I spend way too much time writing pretty comments, and implementing
meme sorting algorithms like bogo sort? Yes.
As I can already code I'm using this as practice for Console-UI Design

"""

import os, sys
import random as rng
import time
import joblib
import re
import csv

# Ensures the program runs from its own location, so relative filepaths don't break
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

default_savefile_path = "save_state.gz"


"""
General project guide:
Konsolen basiert

Kategorien erfassen
Titel hinzufügen, sortieren, suchen
Favoriten verwalten

"""

#=====================================================================#
## Here we put our beautiful, fantastic, amazing class definitions ####
#=====================================================================#

class User:
    def __init__(self) -> None:
        self.username = "Guest User"
        self.favorite_songs = []
        self.favorite_albums = [] # Currently unused
        self.settings = {"sort":"default",
                         "playback":"sequential"}
    
    def set_username(self, new_username:str) -> None:
        self.username = new_username
    
    def set_sort(self, mode:str="default") -> None:
        mode = mode.lower()
        if mode in ["default", "bogo", "stalin", "bogostalin"]:
            self.settings["sort"] = mode
        else:
            raise Exception(f"User.set_sort received mode=\"{mode}\".\nSupported options are: default, bogo, stalin, bogostalin")
    

    def sort_readable(self) -> str:
        match self.settings["sort"]:
            case "default":
                return "Default Sort"
            case "bogo":
                return"Bogo Sort"
            case "stalin":
                return "Safe Stalin Sort"
            case "bogostalin":
                return "Safe Stalin Bogo Sort"
            case _:
                return "ERROR"


    def set_playback(self, mode:str="sequential") -> None:
        mode = mode.lower()
        if mode in ["sequential", "shuffle", "smartshuffle"]:
            self.settings["playback"] = mode
        else:
            raise Exception(f"User.set_playback received mode=\"{mode}\".\nSupported options are: sequential, shuffle, smartshuffle")
    

    def playback_readable(self) -> str:
        match self.settings["playback"]:
            case "sequential":
                return "None"
            case "shuffle":
                return"Active"
            case "smartshuffle":
                return "Smart"
            case _:
                return "ERROR"


class Song:
    def __init__(self, title:str="N/A", 
                 artist:str="N/A", 
                 genre:str="N/A", 
                 release_date:str="N/A", 
                 favorites:int=0) -> None:
        self.title = title
        self.artist = artist
        self.genre = genre
        self.release_date = release_date
        self.favorites = favorites
    
    def __repr__(self) -> str:
        title = self.title[:25].ljust(25)
        artist = self.artist[:20].center(20)
        genre = self.genre[:15].rjust(15)
        return f"{title} by {artist} | {genre}"
    
    def comparer_get(self, attribute:str):
        match attribute.lower():
            case "title":
                return self.title
            case "artist":
                return self.artist
            case "genre":
                return self.genre
            case "favorites":
                return self.favorites
            case _:
                raise Exception(f"\nSong.comparer_get() received value: \"{attribute}\" for argument attribute!\nAllowed values are:\ntitle, artist, genre, favs")


    def add_to_favorites(self, user:User) -> None:
        # Adding Stuff
        self.favorites += 1
    

    def remove_from_favorites(self, user:User) -> None:
        # Removal Stuff
        self.favorites -= 1


class Album: # UNUSED
    def __init__(self, title:str="N/A",
                 artist:str="N/A", 
                 genre:str="N/A", 
                 release_date:str="N/A", 
                 favorites:int=0, 
                 songs:list[Song]=[]) -> None:
        self.title = title
        self.artist = artist
        self.genre = genre
        self.release_date = release_date
        self.favorites = favorites
        self.songs = songs
    

    def add_to_favorites(self, user:User) -> None:
        # Adding Stuff
        self.favorites += 1
    

    def remove_from_favorites(self, user:User) -> None:
        # Removal Stuff
        self.favorites -= 1


def load_songs_from_csv(filepath: str) -> list:
    """
    This function was generated with GPT because I got lazy.
    It's only used to load a sample list of songs from a csv file, which was also generated with GPT.
    """
    songs = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            song = Song(title=row['title'],
                        artist=row['artist'],
                        genre=row['genre'],
                        release_date=row['release_date'],
                        favorites=int(row['favorites']))
            songs.append(song)
    return songs


#========================#
## Sorting Algorithms ####
#========================#

def get_progress_bar(percentage:float) -> str:
    completed_bar_num = int((percentage * 100) // 2)
    incomplete_bar_num = 50 - completed_bar_num
    return f"{"#" * completed_bar_num}{"=" * incomplete_bar_num}"

def is_sorted(to_check:list, sorted_by:str) -> bool:
    """
    This bit of code wast shamelessly copy-pasted from StackOverflow. (And then altered)
    Returns true if the list is sorted! Else false!
    """
    return all(to_check[i].comparer_get(sorted_by) <= to_check[i+1].comparer_get(sorted_by) for i in range(len(to_check) - 1))

def sorted_percentage(to_check:list, sorted_by:str) -> float:
    """
    This bit of code wast shamelessly copy-pasted from StackOverflow. (And then altered)
    Returns a float between 0-1 showing what percentage of the list is sorted.
    """
    sorted_count = sum(to_check[i].comparer_get(sorted_by) <= to_check[i+1].comparer_get(sorted_by) for i in range(len(to_check) - 1))
    return sorted_count / len(to_check)


def default_sort(to_sort:list, sort_by:str) -> None:
    to_sort.sort(key=lambda x: x.comparer_get(sort_by))

def bogo_sort(to_sort:list, sort_by:str) -> None:
    """
    This is a meme sorting 'algorithm' that shuffles the list, checks if it is now sorted, and repeats until
    the list is fully sorted. Best case Bogo sort has O(n), worst case it has O(∞), on average it has O(n * n!)
    This is also intentionally coded with no regard for performance.
    Use at your own peril.
    """
    start = time.perf_counter()
    is_done = False
    iteration = 0
    while not is_done:
        rng.shuffle(to_sort)

        is_done = is_sorted(to_sort, sort_by)
        percent_sorted = sorted_percentage(to_sort, sort_by)
        now = time.perf_counter()

        print(f"Bogo-ing in Progress: {get_progress_bar(percent_sorted)} {int(percent_sorted * 100)}% Done - {iteration} iterations - {now - start:.5f} seconds", end="\r")
        iteration += 1
    print()


def safe_stalin_sort(to_sort:list, sort_by:str) -> None:
    """
    Stalin Sort: 
    iterate through the list, and send all elements that are not in order to the Gulag (delete them)

    Safe Stalin Sort:
    Keep the removed elements to reintroduce them in some way. (Usually attaching them to the front)
    """
    start = time.perf_counter()
    is_done = False
    iteration = 0
    while not is_done:
        # Identify sorted and unsorted elements
        sorted_list = []
        gulag = []
        
        for i in range(len(to_sort)):
            if i == 0 or to_sort[i].comparer_get(sort_by) >= to_sort[i - 1].comparer_get(sort_by):
                sorted_list.append(to_sort[i])
            else:
                gulag.append(to_sort[i])
        
        # Reintroduce the unsorted elements at the beginning of the list
        to_sort[:] = gulag + sorted_list

        is_done = is_sorted(to_sort, sort_by)
        percent_sorted = sorted_percentage(to_sort, sort_by)
        now = time.perf_counter()

        print(f"Purging Bourgeoisie: {get_progress_bar(percent_sorted)} {int(percent_sorted * 100)}% Done - {iteration} iterations - {now - start:.5f} seconds", end="\r")
        iteration += 1
    print()


def safe_stalin_bogo_sort(to_sort:list, sort_by:str) -> None:
    """
    Stalin Sort: 
    iterate through the list, and send all elements that are not in order to the Gulag (delete them)

    Safe Stalin Sort:
    Keep the removed elements to reintroduce them in some way. (Usually attaching them to the front)

    Safe Stalin Bogo Sort:
    Reintroduction of elements is random :)
    """
    start = time.perf_counter()
    is_done = False
    iteration = 0
    while not is_done:
        # Identify sorted and unsorted elements
        sorted_list = []
        gulag = []
        
        for i in range(len(to_sort)):
            if i == 0 or to_sort[i].comparer_get(sort_by) >= to_sort[i - 1].comparer_get(sort_by):
                sorted_list.append(to_sort[i])
            else:
                gulag.append(to_sort[i])
        
        # Reintroduce the unsorted elements randomly back into society
        for happy_worker in gulag:
            sorted_list.insert(rng.randint(0, len(sorted_list) - 1), happy_worker)

        to_sort[:] = sorted_list

        is_done = is_sorted(to_sort, sort_by)
        percent_sorted = sorted_percentage(to_sort, sort_by)
        now = time.perf_counter()

        print(f"Re-Educating Bourgeoisie into Clowns: {get_progress_bar(percent_sorted)} {int(percent_sorted * 100)}% Done - {iteration} iterations - {now - start:.5f} seconds", end="\r")
        iteration += 1
    print()


def sort_selector(sort:str, to_sort:list, sort_by:str):
    match sort:
        case "default":
            default_sort(to_sort, sort_by)
        case "bogo":
            bogo_sort(to_sort, sort_by)
        case "stalin":
            safe_stalin_sort(to_sort, sort_by)
        case "bogostalin":
            safe_stalin_bogo_sort(to_sort, sort_by)
        case _:
            raise Exception(f"Invalid sorting algorithm! sort = \"{sort}\" but expected one of [default, bogo, stalin, bogostalin]")


#================================#
## Console Menu functionality ####
#================================#

def clear_console() -> None:
    """
    Utility function to clear the console.
    """
    os.system("cls")
    os.system("cls") # Twice to be extra sure, because somtimes it seems to not fully clear


def save_state(filepath:str, state:dict) -> None:
    """
    Saves the state to the specified filepath.
    """
    joblib.dump(state, filepath)


def load_state(filepath:str) -> dict:
    """
    Loads and returns the state stored at the filepath.
    """
    return joblib.load(filepath)


def confirm_dialogue() -> bool:
    while True:
        try:
            response = input("Y / N\n")[0].lower()
        except:
            print("Invalid Input. Try again.")
            continue
        match response:
            case "y":
                return True
            case "n":
                return False
            case _:
                continue


"""
The menu structure is pretty simple: Each menu (and accompanying functionality) runs in a function,
and if the menu is left (closing the menu, changing menu, etc.) the menu function will return an
int corresponding to the next menu to be opened.

List of menu codes:
0 : Exit - This closes the program

1 : Main Menu - Shows some general stats (username, number of songs, albums, and navigation
                to other menus)

2 : Settings - Allows for selection of sorting algorithms, and setting a username

3 : Play Song - View of songs/albums, with option to play them, add or remove from favorites,
                search for songs by name, album, artist. And to Sort by alphabetical name,
                popularity, release date.
                Playing a song can happen sequentially, shuffeled (true random),
                and smart-shuffle (strong focus on remaining in the same genre, only switching
                when an artist has a song in another genre. Has higher preference for favorites
                songs.)

4 : Favorites - Same as the play song menu, but limited to only the favorited songs. No add to
                favorites function (because from where?) but remove from favorites still exists.

"""


def main_menu(state:dict) -> int:
    print(f"GREETINGS {state["User"].username}!".center(100))
    print(f"@{"=" * 100}@")
    print( "Where would you like to go?")
    while True: # Input loop
        try:
            selected = input("Play Songs <P>, Favorites <F>, Settings <S>, Quit <Q>\n")[0].lower()
        except:
            print("Invalid Input. Try again.")
            continue
        match selected:
            case "p":
                return 3
            case "f":
                return 4
            case "s":
                return 2
            case "q":
                return 0
            case _:
                continue


def settings_menu(state:dict) -> int:
    print( "Where setting would you like to adjust?")
    while True: # Input loop
        clear_console()
        try:
            selected = input("Change Username <U>, Change Sorting Algorithm <S>, Run Sort Debug <D>, Return to Main Menu <M>\n")[0].lower()
        except:
            print("Invalid Input. Try again.")
            continue
        match selected:
            case "u":
                new_username = input("What would you like to be called?\n")
                state["User"].set_username(new_username)
                save_state(default_savefile_path, state)
            case "s":
                sorting_settings_menu(state)
                continue
            case "d":
                clear_console()
                print("RUNNING DEBUG SORT ON ALL SORTING ALGORITHMS")
                # Runs each sorting algorithm once to display their performance
                debug_list = []
                for i in range(25):
                    debug_list.append(Song(title=str(i)))

                rng.shuffle(debug_list)
                debug_timer_start = time.perf_counter()
                default_sort(debug_list, "title")
                debug_timer_end = time.perf_counter()
                print(f"Python's Default Sort took {debug_timer_end - debug_timer_start:.8f} seconds.")
                
                rng.shuffle(debug_list)
                safe_stalin_sort(debug_list, "title")

                rng.shuffle(debug_list)
                safe_stalin_bogo_sort(debug_list, "title")

                rng.shuffle(debug_list)
                #bogo_sort(debug_list, "title")
                print("Bogo Sort has been Ommited to respect your time.")
            case "m":
                return 1
            case _:
                continue


def sorting_settings_menu(state:dict) -> None:
    while True: # Input loop
        clear_console()
        print(f"The current Sorting Algorithm is {state["User"].sort_readable()}.")
        print("Select an Algorithm to learn more about it, and select it.")
        try:
            selected = input("Default <D>, Bogo <B>, Safe Stalin <S>, Safe Stalin Bogo <A>, Return to Settings <R>\n")[0].lower()
        except:
            print("Invalid Input. Try again.")
            continue
        match selected:
            case "d":
                clear_console()
                print("## DEFAULT SORT #####")
                print(f"@{"=" * 100}@")
                print("The default sort provided by python.")
                print(f"@{"=" * 100}@")
                print("It's fast!")
                print("Set Default Sort as active?")
                if confirm_dialogue():
                    state["User"].set_sort("default")
                else:
                    continue
            case "b":
                clear_console()
                print("## BOGO SORT #####")
                print(f"@{"=" * 100}@")
                print("Randomly shuffles the list, and then checks if it's sorted. If it's not sorted shuffle again.\nRepeat until list is sorted!")
                print("WARNING: This algorithms runtime is O(n * n!) -> Even for tiny lists this can take several minutes to complete!")
                print("ONLY VIABLE IF YOU'RE A FAN OF GAMBLING! DO NOT USE THIS IF YOU VALUE YOUR TIME!")
                print(f"@{"=" * 100}@")
                print("Absurdly slow. If you're unlucky it will NEVER complete!")
                print("Set Bogo Sort as active?")
                if confirm_dialogue():
                    state["User"].set_sort("bogo")
                else:
                    continue
            case "s":
                clear_console()
                print("## SAFE STALIN SORT #####")
                print(f"@{"=" * 100}@")
                print("Goes through the list and sends all out-of-place elements to the Gulag! The resulting list is shorter, but sorted!")
                print("Safe Stalin Sort then reintroduces the gulag inmates at the front of the list. This process repeats until the full list is sorted.")
                print(f"@{"=" * 100}@")
                print("Can get very slow with larger lists!")
                print("Set Stalin Sort as active?")
                if confirm_dialogue():
                    state["User"].set_sort("stalin")
                else:
                    continue
            case "a":
                clear_console()
                print("## SAFE STALIN BOGO SORT #####")
                print(f"@{"=" * 100}@")
                print("Goes through the list and sends all out-of-place elements to the Gulag! The resulting list is shorter, but sorted!")
                print("Safe Stalin Bogo Sort then reintroduces the gulag inmates at random locations in the list. This process repeats until the full list is sorted.")
                print(f"@{"=" * 100}@")
                print("It's the worst of both worlds! Incredibly slow! But still faster than Bogo Sort!")
                print("Set Stalin Bogo Sort as active?")
                if confirm_dialogue():
                    state["User"].set_sort("bogostalin")
                else:
                    continue
            case "r":
                break
            case _:
                continue
    save_state(default_savefile_path, state)


def play_menu(state:dict, favorites:bool=False) -> int:
    display_space = state["Songs"] if not favorites else state["User"].favorite_songs
    display_slice_min = 0
    display_slice_max = 5
    song_pointer = 0
    song_pointer_max = 4
    now_playing = None
    while True: # Input loop
        clear_console()
        print(f"{" " * 14}{"Song Name".ljust(25)}|{"Artist".center(23)}|{"Genre".center(17)}  || Favorited")
        print(f"@{"=" * 100}@")
        for pointer, song in enumerate(display_space[display_slice_min:display_slice_max]):
            star = "☆"
            if song in state["User"].favorite_songs:
                star = "★"
            
            play_marker = " "
            if song == now_playing:
                play_marker = "="

            if pointer == song_pointer:
                print(f"{" " * 11}>{play_marker}{song}{play_marker}< || {star}")
            else:
                print(f"{" " * 11} {play_marker}{song}{play_marker}  || {star}")

        print(f"@{"=" * 100}@")
        print(f"Now playing: {now_playing}   || Shuffle: {state["User"].playback_readable()}")
        print(f"@{"=" * 100}@")

        try:
            if favorites:
                print("Up <U>, Down <D>, Play/Stop <P>, Shuffle Mode <S>, Remove Favorite <F>, Return to Main Menu <R>")
            else:
                print("Up <U>, Down <D>, Play/Stop <P>, Shuffle Mode <S>, Add/Remove Favorite <F>, Return to Main Menu <R>")
            selected = input("Next Song <N>, Search for Song <?>, Sort <!>\n")[0].lower()
        except:
            print("Invalid Input. Try again.")
            continue
        match selected:
            case "u":
                if display_slice_min > 0 and song_pointer <= 1:
                    display_slice_min -= 1
                    display_slice_max -= 1
                elif display_slice_min >= 0 and song_pointer > 0:
                    song_pointer -= 1
            case "d":
                if display_slice_max < len(display_space) and song_pointer == song_pointer_max - 1:
                    display_slice_min += 1
                    display_slice_max += 1
                elif display_slice_min <= len(display_space) and song_pointer < song_pointer_max:
                    song_pointer += 1
            case "p":
                if now_playing == display_space[display_slice_min + song_pointer]:
                    now_playing = None
                else:
                    now_playing = display_space[display_slice_min + song_pointer]
            case "s":
                modes = ["sequential", "shuffle", "smartshuffle"]
                new_mode = (modes.index(state["User"].settings["playback"]) + 1) % len(modes)
                state["User"].set_playback(modes[new_mode])
            case "f":
                if display_space[display_slice_min + song_pointer] in state["User"].favorite_songs:
                    state["User"].favorite_songs.remove(display_space[display_slice_min + song_pointer])
                else:
                    state["User"].favorite_songs.append(display_space[display_slice_min + song_pointer])
                save_state(default_savefile_path, state)
            case "r":
                return 1
            case "n":
                if now_playing == None:
                    continue
                match state["User"].settings["playback"]:
                    case "sequential":
                        now_playing = display_space[(display_space.index(now_playing) + 1) % len(display_space)]
                    case "shuffle":
                        now_playing = display_space[rng.randint(0, len(display_space))]
                    case "smartshuffle":
                        found_genre_songs = list(filter(lambda song: bool(re.search(now_playing.genre, song.genre)), display_space))
                        found_artist_songs = list(filter(lambda song: bool(re.search(now_playing.artist, song.artist)), display_space))
                        searching = True
                        found_song = None
                        while searching:
                            try:
                                found_song = found_genre_songs[rng.randint(0, len(found_genre_songs))]
                            except:
                                searching = False
                            if rng.random() <= 0.25: # 25% Chance to match the Artist instead of Genre
                                try:
                                    found_song = found_artist_songs[rng.randint(0, len(found_artist_songs))]
                                except:
                                    searching = False
                            if found_song in state["User"].favorite_songs:
                                searching = False
                            elif rng.random() <= 0.45: # 45% Chance to re-shuffle Non-Favorite to find a Favorite instead
                                continue
                            else:
                                searching = False
                        if found_song == None:
                            found_song = display_space[rng.randint(0, len(display_space))]
                        now_playing = found_song
                    case _:
                        now_playing = None
            case "?":
                search_result_index = play_menu_search(state, favorites)
                if search_result_index == None:
                    continue
                display_slice_min = search_result_index
                display_slice_max = display_slice_min + 5
                song_pointer = 0
            case "!":
                play_menu_sort(state, favorites)
            case _:
                continue


def play_menu_search(state:dict, favorites:bool=False) -> int:
    search_space = state["Songs"] if not favorites else state["User"].favorite_songs
    found_songs = []
    display_slice_min = 0
    display_slice_max = 5
    song_pointer = 0
    song_pointer_max = 4
    while True: # Input loop
        clear_console()
        if found_songs == []:
            print("Search by what?")
            try:
                selected = input("Title <T>, Artists <A>, Genre <G>, Release Date <R>, Close Search <C>\n")[0].lower()
            except:
                print("Invalid Input. Try again.")
                continue
            match selected:
                case "t":
                    regex = re.compile(input("Enter Song Title:\n"))
                    found_songs = list(filter(lambda song: bool(re.search(regex, song.title)), search_space))
                    display_slice_max = 5 if len(found_songs) > 5 else len(found_songs) - 1
                    song_pointer_max = 4 if len(found_songs) > 5 else len(found_songs) - 1
                case "a":
                    regex = re.compile(input("Enter Artist Name:\n"))
                    found_songs = list(filter(lambda song: bool(re.search(regex, song.artist)), search_space))
                    display_slice_max = 5 if len(found_songs) > 5 else len(found_songs) - 1
                    song_pointer_max = 4 if len(found_songs) > 5 else len(found_songs) - 1
                case "g":
                    regex = re.compile(input("Enter Genre:\n"))
                    found_songs = list(filter(lambda song: bool(re.search(regex, song.genre)), search_space))
                    display_slice_max = 5 if len(found_songs) > 5 else len(found_songs) - 1
                    song_pointer_max = 4 if len(found_songs) > 5 else len(found_songs) - 1
                case "r":
                    regex = re.compile(input("Enter Release Date:\n"))
                    found_songs = list(filter(lambda song: bool(re.search(regex, song.release_date)), search_space))
                    display_slice_max = 5 if len(found_songs) > 5 else len(found_songs) - 1
                    song_pointer_max = 4 if len(found_songs) > 5 else len(found_songs) - 1
                case "c":
                    return None
                case _:
                    continue
        else:
            if len(found_songs) == 1:
                return search_space.index(found_songs[0])
            print("Select a Song!")
            for pointer, song in enumerate(found_songs[display_slice_min:display_slice_max]):            
                if pointer == song_pointer:
                    print(f"> {song} <")
                else:
                    print(f"  {song}  ")
            try:
                selected = input("Up <U>, Down <D>, Select <S>, Close Search <C>\n")[0].lower()
            except:
                print("Invalid Input. Try again.")
                continue
            match selected:
                case "u":
                    if display_slice_min > 0 and song_pointer <= 1:
                        display_slice_min -= 1
                        display_slice_max -= 1
                    elif display_slice_min >= 0 and song_pointer > 0:
                        song_pointer -= 1
                case "d":
                    if display_slice_max < len(found_songs) and song_pointer == song_pointer_max - 1:
                        display_slice_min += 1
                        display_slice_max += 1
                    elif display_slice_min <= len(found_songs) and song_pointer < song_pointer_max:
                        song_pointer += 1
                case "s":
                    return search_space.index(found_songs[display_slice_min + song_pointer])
                case "c":
                    break
                case _:
                    continue


def play_menu_sort(state:dict, favorites:bool=False) -> None:
    sort_space = state["Songs"] if not favorites else state["User"].favorite_songs
    while True: # Input loop
        print("Sort by what?")
        try:
            selected = input("Title <T>, Artists <A>, Genre <G>, Release Date <R>, Popularity <P>, Close Sort <C>\n")[0].lower()
        except:
            print("Invalid Input. Try again.")
            continue
        match selected:
            case "t":
                sort_selector(state["User"].settings["sort"], sort_space, "title")
            case "a":
                sort_selector(state["User"].settings["sort"], sort_space, "artist")
            case "g":
                sort_selector(state["User"].settings["sort"], sort_space, "genre")
            case "r":
                sort_selector(state["User"].settings["sort"], sort_space, "release_date")
            case "p":
                sort_selector(state["User"].settings["sort"], sort_space, "favorites")
            case "c":
                break
            case _:
                continue


#===================#
## THE MAIN LOOP ####
#===================#

if __name__ == "__main__":
    try:
        state = load_state(default_savefile_path)
    except:
        state = {"User": User(),
                 "Songs": load_songs_from_csv("base_songs.csv"),
                 "Albums": []}
        save_state(default_savefile_path, state)

    status_var = 1
    while True:
        clear_console()
        # UI stuff here
        match status_var:
            case 1:
                status_var = main_menu(state)
            case 2:
                status_var = settings_menu(state)
            case 3:
                status_var = play_menu(state)
            case 4:
                status_var = play_menu(state, True)
            case _:
                status_var = 0
        
        # If we quit, we quit
        if status_var == 0:
            break
    clear_console()
    print(f"@{"=" * 100}@")
    print(f"Goodbye {state["User"].username}!".center(100))
    print(f"@{"=" * 100}@")
    input() # Prevent terminal window from instantly closing

