#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

import random
board = list(range(1,10))
#-------------------

play_game = 1 #Who first: 0-drones, 1-player

mode = 'mid'
#mode = 'easy'
#mode = 'hard'

#-------------------

rospy.init_node('decidion_making', anonymous=True)
pub = rospy.Publisher('/move_dron', String, queue_size=10)

#-------Subscriber--------

def callback(data):

    if play_game == 1:
        rospy.loginfo("I heard %s", data.data)
        board[int(data.data)-1] = 'O'
        index_drone_move = computer_move(board, 'X')
        talker(index_drone_move)
        draw_board(board)
	
        tmp = check_win(board)
        if tmp:
            if tmp == 'O':
                print (tmp, "Player Wins!")
                talker('Player Wins')
                talker('end game')
            if tmp == 'X':
                print(tmp, "Drones Win!")
                talker('Drones Win')
                talker('end game')
            win = True

    if play_game == 0:
        index_drone_move = computer_move(board, 'O')
        talker(index_drone_move)
        draw_board(board)

        rospy.loginfo("I heard %s", data.data)
        board[int(data.data)-1] = 'X'

        tmp = check_win(board)
        if tmp:
            if tmp == 'X':
                print (tmp, "Player Wins!")
                talker('Player Wins')
                talker('end game')
            if tmp == 'O':
                print(tmp, "Drones Win!")
                talker('Drones Win')
                talker('end game')
            win = True

    counter = 0
    for i in range(9):
        if board[i] == 'O' or board[i] == 'X':
            counter += 1
        if counter == 9:
            print ("Draw!")
            talker('No winner')
            talker('end game')


def listener():
    #rospy.Subscriber("/human_turns", String, callback)
    rospy.Subscriber("/human_turns_sim", String, callback)
    rospy.spin()
    return String
#-------------------------

def main(board):
    counter = 0
    win = False
    while not win:
        draw_board(board)
        if counter % 2 == 0:
            print("---Player's move---")
            listener()
            #take_input("O")
        else:
            print("---Drone's move---")
            #take_input("X") #manual input
            index_drone_move = computer_move(board)
            talker(index_drone_move)
        counter += 1

        if counter > 4:
            tmp = check_win(board)
            if tmp:
                if tmp == 'O':
                    print (tmp, "Player Wins!")
                    talker('Player Wins')
                if tmp == 'X':
                    print(tmp, "Drones Wins!")
                    talker('Drones Wins')
                win = True
                break
        if counter == 9:
            print ("Draw!")
            talker('No winner')
            break
        draw_board(board)


def draw_board(board):
    print ("-" * 13)
    for i in range(3):
        print (board[0+i*3], board[1+i*3], board[2+i*3])
        print ("-" * 13)

def check_win(board):
    win_coord = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for each in win_coord:
        if board[each[0]] == board[each[1]] == board[each[2]]:
            return board[each[0]]
    return False

def take_input(player_token):
    valid = False
    while not valid:
        player_answer = input("Where put " + player_token+"? ")
        try:
            player_answer = int(player_answer)
        except:
            print ("It isn't a number?")
            continue
        if player_answer >= 1 and player_answer <= 9:
            if (str(board[player_answer-1]) not in "XO"):
                board[player_answer-1] = player_token
                valid = True
            else:
                print ("Not empty cell")
        else:
            print ("Write number from 1 to 9")


def computer_move(board, symbol):
    move_drone_index = 0
    if mode == 'hard':
        move_drone_index = 0
        return move_drone_index + 1


    if mode == 'easy':
        while True:
            rand_board = random.randint(1, 8)
            if board[rand_board] != 'O' and board[rand_board] != 'X':
                board[rand_board] = symbol
                move_drone_index = rand_board
                break
        return move_drone_index + 1

    if mode == 'mid':
        for n in range(3):

            res, index = can_win(board[3*n], board[3*n+1], board[3*n+2], 'X')
            if res:
                board[3*n + (index-1)] = symbol
                move_drone_index = 3*n + (index-1)
                return move_drone_index + 1

            res, index = can_win(board[n], board[n+3], board[n+6], 'X')
            if res:
                board[n + (index - 1)*3] = symbol
                move_drone_index = n + (index - 1)*3
                return move_drone_index + 1

        res, index = can_win(board[0], board[4], board[8], 'X')
        if res:
            board[(index - 1) * 4] = symbol
            move_drone_index = (index - 1) * 4
            return move_drone_index + 1

        res, index = can_win(board[2], board[4], board[6], 'X')
        if res:
            board[index * 2] = symbol
            move_drone_index = index * 2
            return move_drone_index + 1

        for n in range(3):
            res, index = can_win(board[3 * n], board[3 * n + 1], board[3 * n + 2], 'O')
            if res:
                board[3*n + (index-1)] = symbol
                move_drone_index = 3*n + (index-1)
                return move_drone_index + 1

            res, index = can_win(board[n], board[n+3], board[n+6], 'O')
            if res:
                board[n + (index - 1)*3] = symbol
                move_drone_index = n + (index - 1)*3
                return move_drone_index + 1

        res, index = can_win(board[0], board[4], board[8], 'O')
        if res:
            board[(index - 1) * 4] = symbol
            move_drone_index = (index - 1) * 4
            return move_drone_index + 1

        res, index = can_win(board[2], board[4], board[6], 'O')
        if res:
            board[index * 2] = symbol
            move_drone_index = index * 2
            return move_drone_index + 1

        while True:
            rand_board = random.randint(1, 8)
            if board[rand_board] != 'O' and board[rand_board] != 'X':
                board[rand_board] = symbol
                move_drone_index = rand_board
                break
    return move_drone_index + 1

def can_win(a1,a2,a3,smb):
    res = False
    index = 0
    if a1 == smb and a2 == smb and a3 != 'O' and a3 != 'X':
        index = 3
        res = True
    if a1 == smb and a2 != 'O' and a2 != 'X' and a3 == smb:
        index = 2
        res = True
    if a1 != 'X' and a1 != 'O' and a2 == smb and a3 == smb :
        index = 1
        res = True
    return res, index


def talker(index_drone_move):
    rate = rospy.Rate(10) # 10hz
    hello_str = str(index_drone_move)
    rospy.loginfo(hello_str)
    pub.publish(hello_str)
    rate.sleep()

if __name__ == '__main__':
    try:
        talker('new game')
        listener()
    except rospy.ROSInterruptException:
        pass


