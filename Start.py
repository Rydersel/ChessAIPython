"""
ChessAI Program with 1 move AI
AI Uses Alpha-Beta Algorithm
ChessAI AI Engine inspired by work by Dirk and Sam Liu
I focused mainly on the AI for this project so most of the generic chess board code was not written by me (Specific code is credited)
Special Thanks to mbuffett.com's tutorial on 'Creating a basic chess AI with Python'

"""


import Pieces
import AI_Model
import board
import random as rand

from colorama import Fore

AI_Move_History = []
User_Move_History = []
#Choose Your Opponent
#Each Opponent values different pieces differently.


#Default Config
config = {
    "pawn": 100,
    "rook": 250,
    "knight": 320,
    "queen": 900,
    "bishop": 350,
    "king": 20000
}



while True:

    print(Fore.BLUE + "Please pick an opponent\n")
    print(Fore.CYAN + "Type (0) for default")
    print(Fore.GREEN + "Type (1) for Rob. Rob hates Pawns with a vengence")
    print(Fore.YELLOW + "Type (2) for James. James hates Queens")
    print(Fore.RED + "Type (3) for custom \n")
    opponent_choice = input(Fore.BLUE + "Your Answer:")

    if opponent_choice == ("0"): #Does not modify config
        break

    if opponent_choice == ("1"):
        config["pawn"] = 2000
        print("\n")
        break

    if opponent_choice == ("2"):
        config["queen"] == 20000
        print("\n")
        break

    if opponent_choice == ("3"):
        print("Type 1 to Load your exsisting Config")
        print("Type 2 to create a new Config")
        print("Type 3 to play a random config\n")
        config_choice = input("Answer:")

        if config_choice == "1":
            myfile = open("config.txt", 'r')
            read_config = {}
            for line in myfile:
                key, value = line.strip().split(':')  # Symbol splitting our Key from our Value
                read_config[key.strip()] = value.strip()
            config = read_config
            myfile.close()
            break

        if config_choice == "2":
            config["pawn"] = input("Pawn Value:")
            config["rook"] = input("Rook Value:")
            config["knight"] = input("Knight Value:")
            config["queen"] = input("Queen Value:")
            config["bishop"] = input("Bishop Value:")


            # Save Config
            file = open("Config.txt", "w")
            for key, value in config.items():  # Write to Config
                file.write('%s:%s\n' % (key, value))
            file.close()
            print("\n")
            break

        if config_choice == "3":

            config["pawn"] = rand.randrange(50,500)
            config["rook"] = rand.randrange(100,1000)
            config["knight"] = rand.randrange(100,1000)
            config["queen"] = rand.randrange(200,10000)
            config["bishop"] = rand.randrange(200,1000)
            break
    else:
        print("Invalid Response")
        pass

#Create New Board
board = board.Board.new(weight_dict=config)
print(board.to_string())


# Converts Letter inputs for X axis of board into numbers
def letter_to_xpos(letter):
    letter = letter.upper() #allows both lower and upper case answersz
    if letter == 'A':
        return 0
    if letter == 'B':
        return 1
    if letter == 'C':
        return 2
    if letter == 'D':
        return 3
    if letter == 'E':
        return 4
    if letter == 'F':
        return 5
    if letter == 'G':
        return 6
    if letter == 'H':
        return 7
    else:
        print("Invalid Letter.") #TODO: Fix printing twice

Example_Move_List = ["Example Move: E2 E4", #todo list example 1
                     "Example Move: C2 C4,",
                     "Example Move: G1 F3",
                     "Example Move: D2 D4,"] #Most popular oppening moves acording to the internet.

def get_user_move():
    stop_game_phrases = ["leave",  #Any of these words when typed in will cause the game to quit
                         "stop",
                         "exit",
                         "quit",
                         "i hate this game"]

    print("Example Move:",Example_Move_List[rand.randrange(1,len(Example_Move_List))]) #Chooses random example move
    #todo Example List 2
    move_str = input("Please type your move: ")
    for i in range(0, len(stop_game_phrases)):  #todo List example 3
        if  move_str.lower() == str(stop_game_phrases[i]): #Checks if the answer inputed is on the stop_game_phrases
            print("\n")                                    #If the word is on this list, the game stops
            print("Thanks for playing!\n")
            print("AI Move History:")
            for i in range(0,len(AI_Move_History)):
                print(AI_Move_History[i - 1])
            print("Player Move History:\n")
            for i in range(0,len(User_Move_History)):
                print(User_Move_History[i])
            exit()




    move_str = move_str.replace(" ", "")


#Thank you to Stackoverflow for the following method of verifying if a move is valid.
    try:
        x_from = letter_to_xpos(move_str[0:1]) # X pos of where piece was
        y_from = 8 - int(move_str[1:2]) # Y pos of where piece was
        x_to = letter_to_xpos(move_str[2:3]) # X pos of where piece is going
        y_to = 8 - int(move_str[3:4]) # Y pos of where piece is going
        return AI_Model.Move(x_from, y_from, x_to, y_to, False)

    # If Format is Invalid
    except ValueError:
        print("Invalid format. Example Move: C2 C4")
        return get_user_move()

# Returns a valid move based on the users input.

def get_valid_user_move(board):
    while True:
        valid = False #Move is assumed false until proven true (Guilty until proven innocent)
        move = get_user_move()
        possible_moves = board.get_possible_moves(Pieces.Piece.WHITE)
        # No possible moves
        if (not possible_moves):
            return 0

        for possible_move in possible_moves:
            if (move.equals(possible_move)):
                move.castling_move = possible_move.castling_move
                valid = True
                break

        if valid == True:
            break
        else:
            print("Invalid move.")
    return move




#Main Runtime Loop
while True:

    move = get_valid_user_move(board)
    if (move == 0):
        if (board.is_check(Pieces.Piece.WHITE)):
            print("Checkmate. Black Wins.")
            print("AI Move History:")
            for i in range(0,len(AI_Move_History)):
                print(AI_Move_History[i])
            print("Player Move History:\n")
            for i in range(0,len(User_Move_History)):
                print(User_Move_History[i])
            break
        else:
            print("Stalemate.")
            print("AI Move History:")
            for i in range(0,len(AI_Move_History)):
                print(AI_Move_History[i])
            print("Player Move History:\n")
            for i in range(0,len(User_Move_History)):
                print(User_Move_History[i])
            break

    board.perform_move(move)

    # Reprints Board
    print(board.to_string())
    #Prints out User move
    print("User move: " + move.to_string()+ "\n")
    User_Move_History.append(move.to_string())  #todo List Example 4
   #Trigger AI move
    ai_move = AI_Model.AI.get_ai_move(board, [])

    #IF AI is unable to make a move, then user wins
    if (ai_move == 0):
        if (board.is_check(Pieces.Piece.BLACK)):
            print("Checkmate, White wins\n")
            print("AI Move History:\n")
            for i in len(AI_Move_History):
                print(AI_Move_History[i - 1])
            print("Player Move History:\n")
            for i in len(User_Move_History):
                print(User_Move_History[i - 1])
            exit() #End Game

    #If neither the AI or player can move then the game is a tie.
        else:
            print("Stalemate\n")
            print("AI Move History:")
            for i in len(AI_Move_History):
                print(AI_Move_History[i - 1])
            print("Player Move History:\n")
            for i in len(User_Move_History):
                print(User_Move_History[i - 1])
            exit()  # End Game
            exit() #End Game



    board.perform_move(ai_move)


    #Reprints Board
    print(board.to_string())
    #Prints out what move the AI made
    print("AI Move: " + ai_move.to_string() + "\n")
    AI_Move_History.append(ai_move.to_string())   #todo List Example 5
