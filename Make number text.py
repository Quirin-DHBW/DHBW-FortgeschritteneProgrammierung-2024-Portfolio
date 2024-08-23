import random as rng
import time

# This file was used to visualise some of the numbers related to bogo sort for display purposes.

# The number resulting out of n * n! for n = 100
number = 933262154
potency = 151

written_number = str(number) + "0" * potency
numbery_number = int(written_number)

list_example = [x for x in range(100)]

start = time.perf_counter()
rng.shuffle(list_example)
end = time.perf_counter()

shuffle_time = end - start

average_iteration_time = shuffle_time * numbery_number

print(f"{numbery_number:,} Iterations")
print(f"This would take {average_iteration_time} seconds")

# After asking ChatGPT to break down the time in seconds as "ages of the universe"
biiig = int(4.89e137) # <- times the age of the universe
print(f"{biiig:,}")
 