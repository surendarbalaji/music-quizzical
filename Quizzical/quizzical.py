import random
import time
import json

def registration():
    while True:
        username = input("Enter a username: ")
        password = input("Enter a password: ")

        with open("accounts.json", "r") as file:
            user_data = json.load(file)
        
        if username in user_data:
            userlogin_response = input("Username already exists. Please choose a different username by pressing [enter] or login by typing [login] ").lower()
            if userlogin_response == "login":
                login()
        else:
            user_data[username] = password

            with open("accounts.json", "w") as file:
                json.dump(user_data, file)

            print("You are now on the list")
            tutorial()
            return username
            break

def login():
    while True:
        username = input("Enter a username: ")
        password = input("Enter a password: ")

        with open("accounts.json", "r") as file:
            user_data = json.load(file)

        if username in user_data and user_data[username] == password:
            time.sleep(0.5)
            print("You have been logged in")
            return username
            break

        else:
            userregister_response = input("incorrect username or password. Please try again by pressing [enter] or register with [register] ").lower()
            if userregister_response == "register":
                registration()

def tutorial():
    time.sleep(0.5)
    print("The music quiz gives you an artist and the first letter of each word of one of their songs")
    time.sleep(2)
    print("For example, Bohemian Rhapsody would look like")
    time.sleep(2)
    print("BH by Queen")
    time.sleep(2)
    print("You need to guess the name of the song")
    time.sleep(2)
    print("You have two tries")
    time.sleep(2)
    print("First try gets you 3 points")
    time.sleep(2)
    print("Second try gets you 1")
    time.sleep(2)
    print("If you don't get it within 2, you lose")
    time.sleep(2)
    print("Good luck")
    time.sleep(2)

def question(songs, guesses):
    #chooses a random song and artist pair
    song, artist = random.choice(list(songs.items()))
    #splits the name into a list and iterates through each item taking the first letter and joins them together
    letters = "".join([word[0] for word in song.split()])
    response = input(f"{letters} by {artist}\n")
    
    while guesses > 0:
        if response.lower() == song.lower():
            return True, guesses, song
            break
        elif guesses == 2:
            guesses -= 1
            response = input(f"Incorrect, you have 1 guess remaining. Please try again.\n")
        elif guesses == 1:
            guesses -= 1
            return False, 0, song

def recordscore(username, points):
    with open("leaderboard.json", "r") as file:
        leaderboard = json.load(file)

        #checks if user is in the leaderboard
        if username in leaderboard:
            #checks if user has gotten a new pb
            if points > int(leaderboard[username]):
                leaderboard[username] = int(points)
                print("New highscore!")
            else:
                print(f"Your high score is {leaderboard[username]}")
        else:
            leaderboard[username] = int(points)
        
        #sorts the leaderboard dictionary and prints it before dumping it to file
        sortedleaderboard = sorted(leaderboard.items(), key=lambda x:x[1], reverse = True)
        sortedleaderboard_dict = dict(sortedleaderboard)
        time.sleep(1)

        print("Leaderboard:")
        count = 0
        for username, score in sortedleaderboard_dict.items():
            print(f"{username}: {score}")
            count += 1
            if count == min(len(sortedleaderboard_dict), 5):
                break

        with open("leaderboard.json", "w") as file:
                json.dump(sortedleaderboard_dict, file)
            

points = 0

print("Welcome to the music quiz")
account_response = input("Do you have an account? [y/n] ").lower()
if account_response == "n":
    username = registration()
else:
    username = login()

time.sleep(0.5)
category_choice = int(input("Choose your category. General: type [1], Rock: type [2]\n"))
if category_choice == 1:
    selection = "general"
else:
    selection = "rock"

time.sleep(1)

#initialises the song file into a dictionary
with open("songs.json", "r") as file:
    songs = json.load(file)[selection]

while True:
    guesses = 2
    result, guesses, song = question(songs, guesses)
    del songs[song]
    if result:
        if guesses == 2:
            points += 3
            print("Correct! You have earned 3 points.")
        else:
            ponts =+ 1
            print("Correct! You have earned 1 points")
    else:
        print(f"You have lost. You gained {points} points")
        time.sleep(2)
        recordscore(username, points)
        again = input("Play again? [y/n] ").lower()
        if again == "n":
            break