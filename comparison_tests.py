from Portfolio_FortgeschritteneProgrammiertechniken import *

clear_console()
print("RUNNING DEBUG SORT ON ALL SORTING ALGORITHMS")

print("Doing 3 runs:")
for run_num in range(3):
    print("Run", run_num + 1)
    # Runs each sorting algorithm once to display their performance
    debug_list = []
    for i in range(250):
        debug_list.append(Song(title=str(i)))
    print("List size: 250")

    rng.shuffle(debug_list)
    debug_timer_start = time.perf_counter()
    default_sort(debug_list, "title")
    debug_timer_end = time.perf_counter()
    print(f"Python's Default Sort took {debug_timer_end - debug_timer_start:.8f} seconds.")

    rng.shuffle(debug_list)
    safe_stalin_sort(debug_list, "title")

    rng.shuffle(debug_list)
    safe_stalin_bogo_sort(debug_list, "title")


    ## SEARCH ALGORITHMS #####
    debug_list = []
    for i in range(1000):
        debug_list.append(Song(title=str(i)))
    rng.shuffle(debug_list)
    print("List size: 1000")

    regex = re.compile("5") # Linear Search for Song "5"
    debug_timer_start = time.perf_counter()
    found_songs = list(filter(lambda song: bool(re.search(regex, song.title)), debug_list))
    debug_timer_end = time.perf_counter()
    print(f"Linear Search took {debug_timer_end - debug_timer_start:.8f} seconds.")


    def binary_search(to_search, target):
        default_sort(to_search, "title")

        left, right = 0, len(to_search) - 1
        
        while left <= right:
            mid = (left + right) // 2
            mid_song = to_search[mid]
            
            if mid_song.title == target:
                return mid_song  # Target song found, return the Song object
            elif mid_song.title < target:
                left = mid + 1  # Continue search in the right half
            else:
                right = mid - 1  # Continue search in the left half
        
        return None  # Target song not found in the list

    debug_timer_start = time.perf_counter()
    found_song = binary_search(debug_list, "5")
    debug_timer_end = time.perf_counter()
    print(f"Binary Search took {debug_timer_end - debug_timer_start:.8f} seconds.")



print("Doing Bogo runs last because they take forever...")
print("Reducing List size to 10 for Bogo Sort demonstration...")
for _ in range(3):
    debug_list = []
    for i in range(10):
        debug_list.append(Song(title=str(i)))
    rng.shuffle(debug_list)
    bogo_sort(debug_list, "title")