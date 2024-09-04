# Documentation for the Portfolioprojekt on the Topic "Fortgeschrittene Programmiertechniken"

---

|Index|
|:-|
|[**Installation**](#installation)|
|[↳ Requirements](#requirements)|
|[**Project Description**](#what-is-this-project)|
|[↳ Premise](#premise)|
|[↳ Features](#features)|
|[↳ Premise-relevant features](#premise-relevant-features)|
|[**Concept**](#concept)|
|[**The Plan**](#the-plan)|
|[↳ Stage 1](#plan-stage-1)|
|[↳ Stage 2](#plan-stage-2)|
|[↳ Stage 3](#plan-stage-3)|
|[↳ Stage 4](#plan-stage-4)|
|[**Architecture**](#architecture)|
|[**Algorithms**](#algorithms)|
|[↳ Sorting Algorithms](#sorting-algoritms)|
|[↳ ↳ *Safe Stalin Sort*](#safe-stalin-sort)|
|[↳ ↳ *Bogo Sort*](#bogo-sort)|
|[↳ ↳ *Safe Stalin Bogo Sort*](#safe-stalin-bogo-sort)|
|[↳ Search Algorithms](#search-algorithms)|
|[↳ ↳ *Linear Search*](#linear-search)|
|[↳ ↳ *Binary Search*](#binary-search)|
|[**Runtimes**](#runtimes)|
|[↳ Sorting Runtimes](#sorting-runtimes)|
|[↳ Search Runtimes](#search-runtime)|
|[↳ Runtime Comparison](#runtime-comparison)|


---
---

## Installation

### Requirements
- Python 3.10 and above
- joblib (used to save and load the songlist and user profile)


---
---

## What is this Project?

### Premise
This project was written as the Portfolioprojekt for the class "Fortgeschrittene Programmiertechniken".
This is a Terminal based mockup of an application for playing songs (Like Spotify). It serves as a means to compare the performance of different Sorting algorithms.

### Features
This song player features a Customizable username! "Playing" songs, as well as a Shuffle option!\
On top of the Shuffle option there is also the new and shiny "Smart Shuffle" option, which will enhance your listening experience by playing songs that are more simillar to each other!\
Enjoy the convinience of your very own  Favorites list, allowing you to save the songs you like the most!

### Premise-relevant Features
Find the songs you want with the Song-Search feature, or just sort the entire list!\
Further customize your experience by choosing the Sorting Algorithm underlying the sort, and bask in the glory of Bogo-Sort, Safe Stalin-Sort, and Safe Stalin Bogo-Sort! (More on those [later](#algorithms))


---
---

## Concept

The generic concept is to immitate an application like Spotify: enabling the user to search for songs, sort their songs, have a favorites list, and customize their experience.


---
---

## The Plan

The Plan and it's execution happened in a few stages, outlined and described here.


### Plan Stage 1

**Definition of Desired Features**
- Similar in concept to a [Product Requirements Document](https://en.wikipedia.org/wiki/Product_requirements_document)
- Loosely written as larger multi-line comments inside of the code


### Plan Stage 2

**Definition of Sub-Goals**
- Breaking down of the desired features into individual requirements
- Combining and linking of sub-goals into concrete code targets like functions or classes


### Plan Stage 3

**Initial Framework**
- Creation of classes
- Defining of empty functions (The functions only have their inputs and outputs defined at this stage)
- Writing of main loop, and hooking up the various functions with each other


### Plan Stage 4

**Writing of code**
- Each function is now given functionality to fit into the predefined inputs and outputs
- "UI elements" and functionality is added, and pre-existing functions hooked up


---
---

## Architecture

The UI interacts with a `state` object, which is a dictionary containing the list of all songs and the user object.\
Songs are defined as a custom `Song` class object containing their title, artist/s, genre, and number of favorites. The list of songs represents the actual list of all songs available. To enable the sorting of song objects a `comparer_get()` method was implemented, to enable sorting by different attributes, as a simple `__lt__()` implementation would only allow for a single attribute to be compared.\
The user object is a custom `User` class, which contains the username, their selected settings, and the user's personal favorites list. This was chosen to theoreticall enable multiple different users, though such a feature is not implemented in this project.\
The UI sits on top of this state object, displays it, and allows for it's manipulation.


---
---

## Algorithms


### **Sorting Algoritms**

The algorithms chosen for this project followed no logical reasoning, and were instead chosen because they are funny.


### Safe Stalin Sort

Stalin sort is a highly efficient but lossy sorting algorithm, in which we go through the list and any object that is not in line simply gets deleted (aka. sent to the gulag, hence the name) leaving a fully sorted list.\
The safe version of stalin sort saves the discarded elements in a separate list, which is then appended to the start of the sorted list. This ensures the previously discarded elements have another chance to be sorted into the list in the next iteration. This process repeats until the list is sorted. Safe stalin sort in very inefficient, but does eventually return a fully sorted list.


### Bogo Sort

Bogo sort is potentially both one of the fastest and one of the slowest "algorithms". The list is first shuffled, then we check if the list is sorted. If it is not sorted yet we shuffle again.\
The efficiency of this "algorithm" is based entirely on luck, and has no guaranteed termination, meaning it can potentially run indefinitely. This does also mean that in can complete after just a single iteration.


### Safe Stalin Bogo Sort

Safe stalin bogo sort combines aspects of both safe stalin sort and bogo sort. The main loop is the same as that of safe stalin sort, however the discarded elements are not appended to the front of the list anymore. Instead the discarded elements are inserted at random locations in the sorted list, effectively un-sorting to some degree.


### **Search Algorithms**

Due to constraints in the UI the search algorithms available for use in this project were very limited under consideration of efficiency. (In stark contrast to the sorting algorithms.)


### Linear Search

The simple and naive method; We iterate through the list, check each element for a match, and then stop when we find a solution. To enable more comfortable search for the user we instead gather all matching songs to be displayed, at the cost of the potential early termination, for cases like searching by author where we want all songs by that artists, and not just the first we find.


### Binary Search

As the list of songs can be sorted relatively easily, a binary search allows for the highly efficient pinpointing of a specific songs location. This does not allow for the finding of multiple songs according to some criteria, instead finding one single song at incredible speeds.


---
---

## Runtimes


### Sorting Runtimes

Stalin Sort has a runtime of **O(n)** and a theoretical average memory efficiency of **O((1 - c) * n)** where **0 <= c <= 1** is the relative amount of elements dropped. This means Stalin Sort *reduces* the memory used after sorting on average.\
[Safe stalin Sort](#safe-stalin-sort) has an entirel different runtime, and no longer affects memory, as the "gulag" list will always just contain the missing elements, requiring no extra space. The average runtime of Safe Stalin Sort is **O(n log n)** as the otherwise discarded elements are appended to the front of the list, meaning they can potentially cause the rest of the following list to be discarded, turning it into a "find the longest ordered sequence" problem which has O(n log n).

Bogo Sort has one of the best and worst runtimes possible, namely it *can* be **O(1)** (or **O(n)** if the process of shufling is counted) in the best case where the first time the List is shuffled, the list is sorted. In the worst case Bogo sort has **O(∞)** as it just never completes. This is because Bogo sort has no guaranteed termination. On average Bogo sort comes out to **O(n * n!)** runtime, which even for small lists quickly bloats the average number of iterations needed to intractible proportions e.g.: for `n = 100` the **average** runtime will be `9.33e159` or `9,332,621,540,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000` Iterations, which would take about `2.1278321843233425e155` seconds, or roughly ***488,999,999,999,999,959,869,766,710,050,077,941,711,847,962,164,311,733,691,123,213,476,623,647,178,359,731,496,524,388,255,494,309,661,368,420,463,734,458,952,706,089,793,143,963,648 TIMES THE CURRENT AGE OF THE UNIVERSE***. Needless to say one should never use Bogo sort.

[Safe Stalin Bogo Sort](#safe-stalin-bogo-sort) has **O(n^2)** as the discarded elements are randomly shuffled back into the list, leading to roughly half of the list being sorted before the algorithm gets "stuck" due to the random insertion, requiring elements to be inserted in the correct location which shrinks with each iteration.


### Search Runtime

The [Linear Search](#linear-search) has a time efficiency of **O(n)** and requires no additional memory (besides where the solution is stored) as we simply check all **n** elements once. This does mean it doesn't scale great, but it is good enough for the smaller sets of songs used here.

The [Binary Search](#binary-search) has a time efficiency of **O(log n)** as it keeps halving the search space each step. As this halfing doesn't create new lists the memory used doesn't change. As Binary Search can't fulfill the requirements of the Project as previously described. A demonstration/comparison of Binary Search is Provided in the `comparison_tests.py` among other things.


### Runtime Comparison

The values in this Table are the average from 3 runs. To get these values simply run `comparison_tests.py`

|Algorithm|Time (in seconds)|List Size|
|:-|-:|-:|
|Python Default|0.0000695 sec|250|
|Safe Stalin|0.29246 sec|250|
|Safe Bogo Stalin|2.77519 sec|250|
|Bogo|90+ sec|10|
|Linear Search|0.0008008 sec|1000|
|Binary Search|0.0002492 sec|1000|


---
---

