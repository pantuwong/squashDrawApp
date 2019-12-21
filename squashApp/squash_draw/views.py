from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.utils.encoding import smart_str

from .models import Player, Schedule, RankHistory

from random import randint
from datetime import datetime

from .createXLSX import createXLSXSchedule
import os.path

def convert_date( str_date ):
    """
    This function converts dd/mm/yyyy to yyyy-mm-dd
    """
    return '{}-{}-{}'.format( str_date[6:10], str_date[3:5] , str_date[0:2] )

# Function to convert the date format 
def convert24(str1): 

    # Checking if last two elements of time 
    # is AM and first two elements are 12 
    if str1[-2:] == "AM" and str1[:2] == "12": 
        return "00" + str1[2:-2] 

    # remove the AM     
    elif str1[-2:] == "AM": 
        return str1[:-2] 

    # Checking if last two elements of time 
    # is PM and first two elements are 12    
    elif str1[-2:] == "PM" and str1[:2] == "12": 
        return str1[:-2] 

    else: 

        # add 12 to hours and remove PM 
        return str(int(str1[:2]) + 12) + str1[2:8] 

def generate_12_34_56( junior_player_list, senior_player_list, junior_player_twice_list, senior_player_twice_list, sc_order, sc_date ):
    """
    This is the function to generate schedule by using
        12,34,56, ... pattern.
    """
    # calculate for junior
    junior_schedule_list = []
    junior_time = ['15:30', '15:30', '15:30',
                    '16:00', '16:00', '16:00',
                    '16:30', '16:30', '16:30', 
                    '17:00', '17:00', '17:00'] 

    for index in range(0,len( junior_player_list )-1,2):
        
        # get player1 and player2 
        player1 = junior_player_list[index]
        player2 = junior_player_list[index+1]

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( junior_time ) - 1:
                break
            tentative_time = datetime.strptime( junior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = junior_time[tentative_index]
                junior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1

        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Juniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        junior_schedule_list.append( match_dict )

    # if the last player has no match
    if len( junior_player_list ) > ( len( junior_schedule_list ) * 2 ):

        # get player1
        player1 = junior_player_list[-1]

        # random player
        r = randint(2, 7 if len(junior_player_twice_list) > 7 else len(junior_player_twice_list) )
        player2 = junior_player_twice_list[-1*r]

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( junior_time ) - 1:
                break
            tentative_time = datetime.strptime( junior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = junior_time[tentative_index]
                junior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1


        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Juniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        junior_schedule_list.append( match_dict )

    # calculate for senior
    senior_schedule_list = []
    senior_time = ['17:30', '17:30', '17:30',
                    '18:00', '18:00', '18:00',
                    '18:30', '18:30', '18:30',
                    '19:00', '19:00', '19:00',
                    '19:30', '19:30', '19:30',
                    '20:00', '20:00', '20:00',
                    '20:30', '20:30', '20:30', 
                    '21:00', '21:00', '21:00',
                    '21:30', '21:30', '21:30',
                    '22:00', '22:00', '22:00']
    for index in range(0,len( senior_player_list )-1,2):
        # get player1 and player2
        player1 = senior_player_list[index]
        player2 = senior_player_list[index+1]

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( senior_time ) - 1:
                break
            tentative_time = datetime.strptime( senior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = senior_time[tentative_index]
                senior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1

        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Seniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        senior_schedule_list.append( match_dict )

    # if the last player has no match
    if len( senior_player_list ) > ( len( senior_schedule_list ) * 2 ):

        # get player1
        player1 = senior_player_list[-1]

        # random player
        r = randint(2, 7 if len( senior_player_twice_list ) > 7 else len( senior_player_twice_list ) )
        player2 = senior_player_twice_list[-1*r]

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( senior_time ) - 1:
                break
            tentative_time = datetime.strptime( senior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = senior_time[tentative_index]
                senior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1

        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Seniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        senior_schedule_list.append( match_dict )

    return [junior_schedule_list, senior_schedule_list]


def generate_13_24_57( junior_player_list, senior_player_list, junior_player_twice_list, senior_player_twice_list, sc_order, sc_date ):
    """
    This is the function to generate schedule by using
        13,24,57, ... pattern.
    """
    # calculate for junior
    junior_schedule_list = []
    junior_time = ['15:30', '15:30', '15:30',
                    '16:00', '16:00', '16:00',
                    '16:30', '16:30', '16:30', 
                    '17:00', '17:00', '17:00'] 
    player_index = list( range( len( junior_player_list ) ) )
    for index in range( len( junior_player_list ) ):
    # check index in player index for player1
        if index in player_index:
            player1_index = index
        else:
            continue

        # chck index in player index for player2
        if index+2 in player_index:
            player2_index = index+2
        else:
            continue

        # get player1 and 2
        player1 = junior_player_list[player1_index]
        player2 = junior_player_list[player2_index]

        # remove index form player_index list
        player_index.remove( player1_index )
        player_index.remove( player2_index )

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( junior_time ) - 1:
                break
            tentative_time = datetime.strptime( junior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = junior_time[tentative_index]
                junior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1

        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Juniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        junior_schedule_list.append( match_dict )

    # if there are 2 players left
    if len( player_index ) == 2:
        
        # get player index
        player1_index = player_index[0]
        player2_index = player_index[1]
        
        # get player1 and 2
        player1 = junior_player_list[player1_index]
        player2 = junior_player_list[player2_index]
        player_index.remove(player1_index)
        player_index.remove(player2_index)

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( junior_time ) - 1:
                break
            tentative_time = datetime.strptime( junior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = junior_time[tentative_index]
                junior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1

        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Juniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        junior_schedule_list.append( match_dict )

    if len( player_index ) == 1:
        # get player index
        player1_index = player_index[0]

        # get player1 and 2
        player1 = seior_player_list[player1_index]
        # random player
        r = randint(2, 7 if len(junior_player_twice_list) > 7 else len(junior_player_twice_list) )
        player2 = junior_player_twice_list[-1*r]

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( junior_time ) - 1:
                break
            tentative_time = datetime.strptime( junior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = junior_time[tentative_index]
                junior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1

        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Juniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        junior_schedule_list.append( match_dict )

    # calculate for senior
    senior_schedule_list = []
    senior_time = ['17:30', '17:30', '17:30',
                    '18:00', '18:00', '18:00',
                    '18:30', '18:30', '18:30',
                    '19:00', '19:00', '19:00',
                    '19:30', '19:30', '19:30',
                    '20:00', '20:00', '20:00',
                    '20:30', '20:30', '20:30', 
                    '21:00', '21:00', '21:00',
                    '21:30', '21:30', '21:30',
                    '22:00', '22:00', '22:00']
    player_index = list( range( len( senior_player_list ) ) )
    for index in range( len( senior_player_list ) ):
    # check index in player index for player1
        if index in player_index:
            player1_index = index
        else:
            continue

        # chck index in player index for player2
        if index+2 in player_index:
            player2_index = index+2
        else:
            continue

        # get player1 and 2
        player1 = senior_player_list[player1_index]
        player2 = senior_player_list[player2_index]
        
        # remove player index from the list
        player_index.remove( player1_index )
        player_index.remove( player2_index )

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( senior_time ) - 1:
                break
            tentative_time = datetime.strptime( senior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = senior_time[tentative_index]
                senior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1

        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Seniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        senior_schedule_list.append( match_dict )

    # if there are 2 players left
    if len( player_index ) == 2:
        
        # get player index
        player1_index = player_index[0]
        player2_index = player_index[1]
        
        # get player1 and 2
        player1 = senior_player_list[player1_index]
        player2 = senior_player_list[player2_index]
        player_index.remove(player1_index)
        player_index.remove(player2_index)

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( senior_time ) - 1:
                break
            tentative_time = datetime.strptime( senior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = senior_time[tentative_index]
                senior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1

        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Seniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        senior_schedule_list.append( match_dict )

    if len( player_index ) == 1:
        # get player index
        player1_index = player_index[0]
        
        # get player1 and 2
        player1 = senior_player_list[player1_index]
        # random player
        r = randint(2, 7 if len(senior_player_twice_list) > 7 else len(senior_player_twice_list) )
        player2 = senior_player_twice_list[-1*r]

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( senior_time ) - 1:
                break
            tentative_time = datetime.strptime( senior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = senior_time[tentative_index]
                senior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1

        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Seniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        senior_schedule_list.append( match_dict )
    

    return [junior_schedule_list, senior_schedule_list]

def generate_14_25_36( junior_player_list, senior_player_list, junior_player_twice_list, senior_player_twice_list, sc_order, sc_date ):
    """
    This is the function to generate schedule by using
        14,25,36, ... pattern.
    """
    # calculate for junior
    junior_schedule_list = []
    junior_time = ['15:30', '15:30', '15:30',
                    '16:00', '16:00', '16:00',
                    '16:30', '16:30', '16:30', 
                    '17:00', '17:00', '17:00'] 
    player_index = list( range( len( junior_player_list ) ) )
    for index in range( len( junior_player_list ) ):
    # check index in player index for player1
        if index in player_index:
            player1_index = index
        else:
            continue

        # chck index in player index for player2
        if index+2 in player_index:
            player2_index = index+3
        else:
            continue

        # get player1 and 2
        player1 = junior_player_list[player1_index]
        player2 = junior_player_list[player2_index]

        # remove index form player_index list
        player_index.remove( player1_index )
        player_index.remove( player2_index )

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( junior_time ) - 1:
                break
            tentative_time = datetime.strptime( junior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = junior_time[tentative_index]
                junior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1


        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Juniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        junior_schedule_list.append( match_dict )

    # if there are 3 players left
    if len( player_index ) == 3:
        # get player index
        player1_index = player_index[0]
        player2_index = player_index[-1]
        
        # get player1 and 2
        player1 = junior_player_list[player1_index]
        player2 = junior_player_list[player2_index]
        player_index.remove(player1_index)
        player_index.remove(player2_index)

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( junior_time ) - 1:
                break
            tentative_time = datetime.strptime( junior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = junior_time[tentative_index]
                junior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1


        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Juniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        junior_schedule_list.append( match_dict )

    if len( player_index ) == 2:
        
        # get player index
        player1_index = player_index[0]
        player2_index = player_index[1]
        
        # get player1 and 2
        player1 = junior_player_list[player1_index]
        player2 = junior_player_list[player2_index]
        player_index.remove(player1_index)
        player_index.remove(player2_index)

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( junior_time ) - 1:
                break
            tentative_time = datetime.strptime( junior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = junior_time[tentative_index]
                junior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1


        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Juniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        junior_schedule_list.append( match_dict )

    if len( player_index ) == 1:
        # get player index
        player1_index = player_index[0]

        # get player1 and 2
        player1 = seior_player_list[player1_index]
        # random player
        r = randint(2, 7 if len(junior_player_twice_list) > 7 else len(junior_player_twice_list) )
        player2 = junior_player_twice_list[-1*r]

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( junior_time ) - 1:
                break
            tentative_time = datetime.strptime( junior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = junior_time[tentative_index]
                junior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1

        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Juniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        junior_schedule_list.append( match_dict )

    # calculate for senior
    senior_schedule_list = []
    senior_time = ['17:30', '17:30', '17:30',
                    '18:00', '18:00', '18:00',
                    '18:30', '18:30', '18:30',
                    '19:00', '19:00', '19:00',
                    '19:30', '19:30', '19:30',
                    '20:00', '20:00', '20:00',
                    '20:30', '20:30', '20:30', 
                    '21:00', '21:00', '21:00',
                    '21:30', '21:30', '21:30',
                    '22:00', '22:00', '22:00']
    player_index = list( range( len( senior_player_list ) ) )
    for index in range( len( senior_player_list ) ):
    # check index in player index for player1
        if index in player_index:
            player1_index = index
        else:
            continue

        # chck index in player index for player2
        if index+2 in player_index:
            player2_index = index+3
        else:
            continue

        # get player1 and 2
        player1 = senior_player_list[player1_index]
        player2 = senior_player_list[player2_index]
        
        # remove player index from the list
        player_index.remove( player1_index )
        player_index.remove( player2_index )

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( senior_time ) - 1:
                break
            tentative_time = datetime.strptime( senior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = senior_time[tentative_index]
                senior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1

        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Seniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        senior_schedule_list.append( match_dict )

    # if there are 3 players left
    if len( player_index ) == 3:
        
        # get player index
        player1_index = player_index[0]
        player2_index = player_index[-1]
        
        # get player1 and 2
        player1 = senior_player_list[player1_index]
        player2 = senior_player_list[player2_index]
        player_index.remove(player1_index)
        player_index.remove(player2_index)

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( senior_time ) - 1:
                break
            tentative_time = datetime.strptime( senior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = senior_time[tentative_index]
                senior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1

        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Seniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        senior_schedule_list.append( match_dict )

    # if there are 2 players left
    if len( player_index ) == 2:
        
        # get player index
        player1_index = player_index[0]
        player2_index = player_index[1]
        
        # get player1 and 2
        player1 = senior_player_list[player1_index]
        player2 = senior_player_list[player2_index]
        player_index.remove(player1_index)
        player_index.remove(player2_index)

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( senior_time ) - 1:
                break
            tentative_time = datetime.strptime( senior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = senior_time[tentative_index]
                senior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1

        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Seniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        senior_schedule_list.append( match_dict )

    elif len( player_index ) == 1:
        # get player index
        player1_index = player_index[0]
        
        # get player1 and 2
        player1 = senior_player_list[player1_index]
        # random player
        r = randint(2, 7 if len(senior_player_twice_list) > 7 else len(senior_player_twice_list) )
        player2 = senior_player_twice_list[-1*r]

        # get player1 and player2 time constraint
        p1Time1 = player1.pyTimeMustGreater
        p1Time2 = player1.pyTimeMustLower
        p2Time1 = player2.pyTimeMustGreater
        p2Time2 = player2.pyTimeMustLower

        timeLower = min( p1Time1, p2Time1 )
        timeUpper = max( p1Time2, p2Time2 ) 
        
        tentative_index = 0

        while True:
            if tentative_index > len( senior_time ) - 1:
                break
            tentative_time = datetime.strptime( senior_time[tentative_index], '%H:%M' ).time()
            time_break = True
            if ( timeLower != datetime.strptime('00:00','%H:%M') or tentative_time >= timeLower ) and \
                ( timeUpper != datetime.strptime('00:00','%H:%M')  or tentative_time <= timeUpper ):
                playtime = senior_time[tentative_index]
                senior_time.remove(playtime)
                time_break = False
                break
            else:
                tentative_index += 1

        # create dictionary for players
        match_dict = {
            'match_date': sc_date,
            'match_class' : 'Seniors',
            'player1': player1,
            'player2': player2,
            'match_time' : playtime,
            'time_break': time_break
        }

        # store in list
        senior_schedule_list.append( match_dict )
    
    return [junior_schedule_list, senior_schedule_list]


def generate_schedule( sc_pattern, sc_order, sc_date ):
    """
    This is an interface fucntion to generate schedule
    """

    # retrieve all active players and sorted by rank
    junior_player_list = list( Player.objects.filter( pyStatus='Active', pyClass='Juniors' ).order_by( 'pyRank' ) )
    junior_player_twice_list = list( Player.objects.filter( pyStatus='Active', pyClass='Juniors', pyPlayTwiceFlag=True ).order_by( 'pyRank' ) )
    senior_player_list = list( Player.objects.filter( pyStatus='Active', pyClass='Seniors' ).order_by( 'pyRank' ) )
    senior_player_twice_list = list( Player.objects.filter( pyStatus='Active', pyClass='Seniors', pyPlayTwiceFlag=True ).order_by( 'pyRank' ) )
    
    if sc_order == '2':
        junior_player_list = junior_player_list[::-1]
        junior_player_twice_list = junior_player_twice_list[::-1]
        senior_player_list = senior_player_list[::-1]
        senior_player_twice_list = senior_player_twice_list[::-1]

    if sc_pattern == '1':
        return generate_12_34_56( junior_player_list, senior_player_list, junior_player_twice_list, senior_player_twice_list, sc_order, sc_date )
    elif sc_pattern == '2':
        return generate_13_24_57( junior_player_list, senior_player_list, junior_player_twice_list, senior_player_twice_list,  sc_order, sc_date )
    else:
        return generate_14_25_36( junior_player_list, senior_player_list, junior_player_twice_list, senior_player_twice_list, sc_order, sc_date )

def drawmatch(request):
    """
    View of the interface to create schedule
    """
    return render(request, 'squash_draw/drawmatch.html')


# def drawmatch_backend(request):
#     """
#     View of the backend got from the drawmatch interface
#     """

#     # get value from form
#     schedule_pattern = request.POST.get('pattern')
#     schedule_order = request.POST.get('order')
#     schedule_date = request.POST.get('date')

#     # generate schedule
#     schedule = generate_schedule( schedule_pattern, schedule_order, schedule_date )
#     schedule_list = []
#     for junior_match in schedule[0]:
#         match = Schedule( scDate= convert_date( junior_match['match_date'] ), scTime=junior_match['match_time'], scClass=junior_match['match_class'],
#                             scPlayer1=junior_match['player1'], scPlayer2=junior_match['player2'], scTimeBreak=junior_match['time_break'] )
#         match.save()
#         schedule_list.append({ 'date':junior_match['match_date'], 'time':junior_match['match_time'], 'class':junior_match['match_class'],
#                                 'player1_name': junior_match['player1'].pyName, 'player1_rank': junior_match['player1'].pyRank,
#                                 'player2_name': junior_match['player2'].pyName, 'player2_rank': junior_match['player2'].pyRank,
#                                 'time_break': junior_match['time_break'] })

#     for senior_match in schedule[1]:
#         match = Schedule( scDate= convert_date( senior_match['match_date'] ), scTime=senior_match['match_time'], scClass=senior_match['match_class'],
#                             scPlayer1=senior_match['player1'], scPlayer2=senior_match['player2'], scTimeBreak=senior_match['time_break'])
#         match.save()
#         schedule_list.append({ 'date':senior_match['match_date'], 'time':senior_match['match_time'], 'class':senior_match['match_class'],
#                                 'player1_name': senior_match['player1'].pyName, 'player1_rank': senior_match['player1'].pyRank,
#                                 'player2_name': senior_match['player2'].pyName, 'player2_rank': senior_match['player2'].pyRank,
#                                 'time_break': senior_match['time_break']  })

#     context = {'schedule':schedule_list}
#     return render(request, 'squash_draw/viewschedule.html', context)

def generate_pdf(request):
    """
    This view is to generate pdf for the schedule in specific date
    """

    # query distict date from schedule table
    date_obj_list = Schedule.objects.order_by('scDate').values_list('scDate').distinct()
    date_list = [ d[0].strftime( '%d/%m/%Y' ) for d in date_obj_list ]
    
    # create context
    context = { 'datelist':date_list }

    return render(request, 'squash_draw/genpdf.html', context)

def genpdf_backend(request):
    """
    This is backend to generate pdf file
    """

    # get value from form
    schedule_date = request.POST.get('date')

    # get schedule information0
    sc_obj_list = Schedule.objects.filter( scDate=convert_date(schedule_date) )
    
    # create dictionary for schedule
    junior_matches_list = []
    senior_matches_list = []
    for sc in sc_obj_list:
        sc.scDraft = False
        sc.save()
        
        match = {
            'time': sc.scTime.strftime("%I:%M %p"),
            'p1name': sc.scPlayer1Name,
            'p1rank': sc.scPlayer1Rank,
            'p1score': sc.scPlayer1Score,
            'p2name': sc.scPlayer2Name,
            'p2rank': sc.scPlayer2Rank,
            'p2score': sc.scPlayer2Score,
            'break_rule': sc.scTimeBreak
        }
        if sc.scClass == 'Juniors':
            junior_matches_list.append(match)
        else:
            senior_matches_list.append(match)

        data = {
            'date': schedule_date,
            'senior': senior_matches_list,
            'junior': junior_matches_list
        }

    path = os.path.abspath(os.path.join(os.pardir,'squashApp/static/xlsx/'))

    createXLSXSchedule( data, path)
    
    file_name = 'schedule_{}.xlsx'.format( data['date'].replace('/','_',3))

    file_path = os.path.join(path, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def index(request):
    """
    This view is index page
    """

    return render(request, 'squash_draw/index.html')

def record_score(request):
    """
    This view is for displaying a form to record score
    """

    # get schedule information0
    sc_obj_list = Schedule.objects.filter(scDraft = "False").order_by( 'scDate', 'scTime' )

    # create dictionary for schedule
    schedule_list = []
    for sc in sc_obj_list:

        schedule_list.append({ 
            'date':sc.scDate.strftime("%d/%m/%Y"), 
            'time':sc.scTime.strftime("%I:%M %p"), 
            'class':sc.scClass,
            'player1_name': sc.scPlayer1Name, 
            'player1_rank': sc.scPlayer1Rank,
            'player1_score': sc.scPlayer1Score,
            'player2_name': sc.scPlayer2Name, 
            'player2_rank': sc.scPlayer2Rank,
            'player2_score': sc.scPlayer2Score,
            'time_break': sc.scTimeBreak,
            'id': sc.id 
        })

    context = {'schedule':schedule_list}
    return render(request, 'squash_draw/record_score.html', context)

def view_players(request):
    """
    This view is for displaying all players
    """
    # get all players
    s_players = Player.objects.all().filter(pyClass='Seniors').order_by('pyRank')
    j_players = Player.objects.all().filter(pyClass='Juniors').order_by('pyRank')

    # for each player, create list of dictionary
    player_list = []
    for p in s_players:
        player_list.append({
            'id':p.id,
            'class':p.pyClass,
            'rank':p.pyRank,
            'name':p.pyName,
            'grade':p.pyGrade if p.pyGrade else '-',
            'point':p.pyPoint if p.pyPoint else '-',
            'timelower':'-' if p.pyTimeMustGreater.strftime("%H:%M") == '00:00' else p.pyTimeMustGreater.strftime("%H:%M"),
            'timeupper':'-' if p.pyTimeMustLower.strftime("%H:%M") == '00:00' else p.pyTimeMustLower.strftime("%H:%M"),
            'note':p.pyNote if p.pyNote else '-',
            'member':'Yes' if p.pyMemberFlag else 'No',
            'status':p.pyStatus
        })
    
    for p in j_players:
        player_list.append({
            'id':p.id,
            'class':p.pyClass,
            'rank':p.pyRank,
            'name':p.pyName,
            'grade':p.pyGrade if p.pyGrade else '-',
            'point':p.pyPoint if p.pyPoint else '-',
            'timelower':'-' if p.pyTimeMustGreater.strftime("%H:%M") == '00:00' else p.pyTimeMustGreater.strftime("%H:%M"),
            'timeupper':'-' if p.pyTimeMustLower.strftime("%H:%M") == '00:00' else p.pyTimeMustLower.strftime("%H:%M"),
            'note':p.pyNote if p.pyNote else '-',
            'member':'Yes' if p.pyMemberFlag else 'No',
            'status':p.pyStatus
        })

    context={'players':player_list}

    return render(request, 'squash_draw/viewplayer.html', context)


def record_score_backend(request):
    """
    This view is for displaying a form to record score
    """

    try:
        # get all players
        all_juniors = Player.objects.filter( pyClass='Juniors' ).order_by( 'pyRank' )
        all_seniors = Player.objects.filter( pyClass='Seniors' ).order_by( 'pyRank' )

        # create data structure for swap
        j_list = []
        for j in all_juniors:
            j_list.append(j)
        
        s_list = []
        for s in all_seniors:
            s_list.append(s)

        # get all possible post data(keys)
        keys = list(request.POST.keys())
        keys.sort()

        # get all matches
        matches = Schedule.objects.all()
        matches_dict = {}
        for m in matches:
            matches_dict[m.id] = m

        # for each key
        for k in keys:
            # if it is a key of p1
            if 'p1' in k:
                # get match id
                match_id = k[3:]
            
                # get score
                p1_score = request.POST.get(k)
                p2_score = request.POST.get('p2_'+match_id)
                # get match get
                match = matches_dict[int(match_id)]
                match.scPlayer1Score = int(p1_score)
                match.scPlayer2Score = int(p2_score)
                match.scPlayer1Rank = match.scPlayer1.pyRank
                match.scPlayer2Rank = match.scPlayer2.pyRank
                match.save()
            
                # get p1 and p2
                if match.scPlayer1:
                    p1 = match.scPlayer1
                else:
                    p1 = None
                    for p in j_list:
                        if p.pyName == match.scPlayer1Name:
                            p1 = p
                            break
                    if not p1:
                        for p in s_list:
                            if p.pyName == match.scPlayer1Name:
                                p1 = p
                                break
                    
                if match.scPlayer2:
                    p2 = match.scPlayer2
                else:
                    p2 = None
                    for p in j_list:
                        if p.pyName == match.scPlayer2Name:
                            p2 = p
                            break
                    if not p2:
                        for p in s_list:
                            if p.pyName == match.scPlayer2Name:
                                p12 = p
                                break
                        
                if p1.pyClass == 'Juniors':
                    p1_index = j_list.index(p1)
                    p2_index = j_list.index(p2)
                    if p1_score > p2_score and p1_index > p2_index:
                        j_list.remove(p1)
                        j_list.insert(p2_index, p1)
                    elif p2_score > p1_score and p2_index > p1_index:
                        j_list.remove(p2)
                        j_list.insert(p1_index, p2)
                else:
                    p1_index = s_list.index(p1)
                    p2_index = s_list.index(p2)
                    if p1_score > p2_score and p1_index > p2_index:
                        s_list.remove(p1)
                        s_list.insert(p2_index, p1)
                    elif p2_score > p1_score and p2_index > p1_index:
                        s_list.remove(p2)
                        s_list.insert(p1_index, p2)
            else:
                continue
            
        # update junior and senior rank
        rank = 1
        for j in j_list:
            j.pyRank = rank
            j.save()
            rank += 1
        
        rank = 1
        for s in s_list:
            s.pyRank = rank
            s.save()
            rank += 1

        return render(request, 'squash_draw/success.html')
    
    except Exception as e:
        print(e)
        return render(request, 'squash_draw/fail.html')

def delete_player(request):
    """
    This view delete player from table
    """

    # get player id
    id = request.POST.get('id')

    # get player with that id
    p = Player.objects.all().filter(id=id)

    try:
        # copy data before delete
        all_sc = Schedule.objects.all().filter(scPlayer1=id)
        for sc in all_sc:
            sc.scPlayer1Name = sc.scPlayer1.pyName
            if not sc.scPlayer1Rank:
                sc.scPlayer1Rank = sc.scPlayer1.pyRank
            sc.save()

        all_sc = Schedule.objects.all().filter(scPlayer2=id)
        for sc in all_sc:
            sc.scPlayer2Name = sc.scPlayer2.pyName
            if not sc.scPlayer2Rank:
                sc.scPlayer2Rank = sc.scPlayer2.pyRank
            sc.save()
            
        all_rh = RankHistory.objects.all().filter(rhPlayer=id)
        for rh in all_rh:
            rh.rhPlayerName = rh.rhPlayer.pyName
            rh.save()

        p.delete()
        return render(request, 'squash_draw/success.html')
    
    except Exception as e:
        print(e)
        return render(request, 'squash_draw/fail.html')

def add_player(request):
    """
    This view creates form for adding new player
    """
    
    # if no post data, create form
    if not request.POST.get('pyName'):
        return render(request, 'squash_draw/add_player.html')
    else:
        try:
            # perform saving to database
            p = Player(
                pyClass=request.POST.get('pyClass'),
                pyName=request.POST.get('pyName'),
                pyRank=request.POST.get('pyRank'),
                pyGradedFlag=True if request.POST.get('pyGrade') else False,
                pyGrade=request.POST.get('pyGrade') if request.POST.get('pyGrade') else None,
                pyPoint=request.POST.get('pyPoint') if request.POST.get('pyPoint') else None,
                pyNote=request.POST.get('pyNote'),
                pyTimeMustGreater=request.POST.get('timelower') if request.POST.get('timelower') else '00:00',
                pyTimeMustLower=request.POST.get('timeupper') if request.POST.get('timeupper') else '00:00',
                pyMemberFlag=True if request.POST.get('pyMemberFlag')=='1' else False,
                pyStatus=request.POST.get('pyStatus'),
                pyPlayTwiceFlag=True if request.POST.get('pyPlayTwiceFlag')=='1' else False,
                pySquashCode=request.POST.get('pySquashCode')
            )
            p.save()
            return render(request, 'squash_draw/success.html')
        except Exception as e:
            print(e)
            return render(request, 'squash_draw/fail.html')

def fail(request):
    return render(request, 'squash_draw/fail.html')

def success(request):
    return render(request, 'squash_draw/success.html')

def edit_player(request):
    """
    This view is used to edit the player
    """

    # get id from post data
    id = request.GET.get('id')

    # get player data
    player_data = Player.objects.all().filter(id=id)[0]

    # create dictionary context
    context = {
        'id':id,
        'pyClass':player_data.pyClass,
        'pyName':player_data.pyName or '',
        'pyRank':player_data.pyRank,
        'pyPoint':player_data.pyPoint or '',
        'pyStatus':player_data.pyStatus,
        'pySquashCode':player_data.pySquashCode or '',
        'pyGrade':player_data.pyGrade or '',
        'timelower':'' if player_data.pyTimeMustGreater.strftime("%H:%M") == '00:00' else player_data.pyTimeMustGreater.strftime("%H:%M"),
        'timeupper':'' if player_data.pyTimeMustLower.strftime("%H:%M") == '00:00' else player_data.pyTimeMustLower.strftime("%H:%M"),
        'pyMemberFlag':player_data.pyMemberFlag,
        'pyPlayTwiceFlag':player_data.pyPlayTwiceFlag,
        'pyNote':player_data.pyNote or ''
    }
    print(context)
    return render(request, 'squash_draw/edit_player.html', context)

def view_player(request):
    """
    This view is used to edit the player
    """

    # get id from post data
    id = request.GET.get('id')

    # get player data
    player_data = Player.objects.all().filter(id=id)[0]

    # create dictionary context
    context = {
        'id':id,
        'pyClass':player_data.pyClass,
        'pyName':player_data.pyName or '-',
        'pyRank':player_data.pyRank,
        'pyPoint':player_data.pyPoint or '-',
        'pyStatus':player_data.pyStatus,
        'pySquashCode':player_data.pySquashCode or '-',
        'pyGrade':player_data.pyGrade or '-',
        'timelower':'-' if player_data.pyTimeMustGreater.strftime("%H:%M") == '00:00' else player_data.pyTimeMustGreater.strftime("%I:%M %p"),
        'timeupper':'-' if player_data.pyTimeMustLower.strftime("%H:M") == '00:00' else player_data.pyTimeMustLower.strftime("%I:%M %p"),
        'pyMemberFlag': 'Yes' if player_data.pyMemberFlag else 'No',
        'pyPlayTwiceFlag': 'Yes' if player_data.pyPlayTwiceFlag else 'No',
        'pyNote':player_data.pyNote or '-'
    }

    return render(request, 'squash_draw/view_player.html', context)

def edit_player_backend(request):
    """
    This view is used to edit the player
    """

    try:

        # get id from post data
        id = request.POST.get('id')

        # get player data
        player_data = Player.objects.all().filter(id=id)[0]

        # edit player data
        player_data.pyClass=request.POST.get('pyClass')
        player_data.pyName=request.POST.get('pyName')
        player_data.pyRank=request.POST.get('pyRank')
        player_data.pyGradedFlag=True if request.POST.get('pyGrade') else False
        player_data.pyGrade= request.POST.get('pyGrade') if request.POST.get('pyGrade') else None
        player_data.pyPoint= request.POST.get('pyPoint') if request.POST.get('pyPoint') else None
        player_data.pyNote=request.POST.get('pyNote')
        player_data.pyTimeMustGreater=request.POST.get('timelower') if request.POST.get('timelower') else '00:00'
        player_data.pyTimeMustLower=request.POST.get('timeupper') if request.POST.get('timeupper') else '00:00'
        player_data.pyMemberFlag=True if request.POST.get('pyMemberFlag')=='1' else False
        player_data.pyStatus=request.POST.get('pyStatus')
        player_data.pyPlayTwiceFlag=True if request.POST.get('pyPlayTwiceFlag')=='1' else False
        player_data.pySquashCode=request.POST.get('pySquashCode')
        player_data.save()
        return render(request, 'squash_draw/success.html')
    
    except Exception as e:
        print(e)
        return render(request, 'squash_draw/fail.html')
    
def match_history(request):
    """
    This views is used to generate match history
    """

    # get schedule and filter only get completed score
    #   order by date, newer first
    matches = Schedule.objects.all().exclude( scPlayer1Score = 0, scPlayer2Score = 0 ).order_by('scDate', 'scTime')

    # create context dictionary
    context = {}
    matches_list = []
    for m in matches:
        
        matches_list.append({
            'date':m.scDate.strftime("%d/%m/%Y"), 
            'time':m.scTime.strftime("%I:%M %p"), 
            'class':m.scClass,
            'player1_name': m.scPlayer1Name, 
            'player1_rank': m.scPlayer1Rank,
            'player1_score': m.scPlayer1Score,
            'player2_name': m.scPlayer2Name, 
            'player2_rank': m.scPlayer2Rank,
            'player2_score': m.scPlayer2Score,
            'time_break': m.scTimeBreak,
            'id': m.id 
        })
    context['matches'] = matches_list

    return render(request, 'squash_draw/match_history.html', context)

def edit_schedule(request):
    """
    This views is used to edit the schedule
    """

    # get date of draw from POST or GET
    match_date = request.POST.get('date') or request.GET.get('date')

    # get matches info from database
    matches = Schedule.objects.filter( scDate=convert_date(match_date) ).exclude( scPlayer1 = None, scPlayer2 = None ).order_by( 'scTime' )

    # create context dictionary
    match_list = []
    draft = False
    for m in matches:
        if m.scDraft:
            draft=True
        match_list.append({
            'date':m.scDate.strftime("%d/%m/%Y"), 
            'time':m.scTime.strftime('%H:%M'), 
            'class':m.scClass,
            'player1': m.scPlayer1.id,
            'player2': m.scPlayer2.id,
            'time_break': m.scTimeBreak,
            'id':m.id
        })
    
    # get players
    players = Player.objects.all()
    player_list = []
    for p in players:
        player_list.append({
            'id':p.id,
            'name':p.pyName
        })
    
    context = {'matches':match_list, 'players':player_list, 'draft':draft}

    return render(request, 'squash_draw/edit_schedule.html', context)

def save_schedule(request):
    """
    This views is used to save schedule as a draftr
    """

    try:
        match_date = request.POST.get('date') or request.GET.get('date')

        # get all POST key
        all_keys = request.POST.keys()

        # create structured data
        data = {}
        for k in all_keys:
            if not '__' in k:
                continue
            
            id = k.split("__",1)[1]
            info = k.split("__",)[0]

            if not id in data:
                data[id] = {}
            
            data[id][info] = request.POST.get(k)
            
        # process each data
        for d in data:
            # if new in d, save new match
            if 'new' in d:
                
                # query player information
                p1 = Player.objects.filter(id=data[d]['scPlayer1'])[0]
                p1_timelower = p1.pyTimeMustGreater
                p1_timeupper = p1.pyTimeMustLower

                p2 = Player.objects.filter(id=data[d]['scPlayer2'])[0]
                p2_timelower = p2.pyTimeMustGreater
                p2_timeupper = p2.pyTimeMustLower

                follow_time = False
                m_time = datetime.strptime( data[d]['scTime'], '%H:%M' ).time()
                if ( p1_timelower != datetime.strptime('00:00','%H:%M') or m_time >= p1_timelower ) and \
                    ( p1_timeupper != datetime.strptime('00:00','%H:%M')  or m_time <= p1_timeupper ) and \
                    ( p2_timelower != datetime.strptime('00:00','%H:%M') or m_time >= p2_timelower ) and \
                    ( p2_timeupper != datetime.strptime('00:00','%H:%M')  or m_time <= p2_timeupper ):
                    follow_time = True
                
                match = Schedule( scDate=convert_date(match_date), 
                                scTime=m_time, 
                                scClass=data[d]['scClass'], 
                                scPlayer1=p1, 
                                scPlayer2=p2,
                                scPlayer1Name=p1.pyName,
                                scPlayer1Rank=p1.pyRank,
                                scPlayer2Name=p2.pyName,
                                scPlayer2Rank=p2.pyRank, 
                                scTimeBreak=not follow_time)
                
                if 'Final' in request.POST.get('action'):
                    print('in')
                    match.scDraft = False     
                match.save()
            
            else:
                # query player information
                p1 = Player.objects.filter(id=data[d]['scPlayer1'])[0]
                p1_timelower = p1.pyTimeMustGreater
                p1_timeupper = p1.pyTimeMustLower

                p2 = Player.objects.filter(id=data[d]['scPlayer2'])[0]
                p2_timelower = p2.pyTimeMustGreater
                p2_timeupper = p2.pyTimeMustLower

                follow_time = False
                m_time = datetime.strptime( data[d]['scTime'], '%H:%M' ).time()
                if ( p1_timelower != datetime.strptime('00:00','%H:%M') or m_time >= p1_timelower ) and \
                    ( p1_timeupper != datetime.strptime('00:00','%H:%M')  or m_time <= p1_timeupper ) and \
                    ( p2_timelower != datetime.strptime('00:00','%H:%M') or m_time >= p2_timelower ) and \
                    ( p2_timeupper != datetime.strptime('00:00','%H:%M')  or m_time <= p2_timeupper ):
                    follow_time = True

                sc = Schedule.objects.filter(id=d)[0]
                sc.Time = m_time
                sc.scClass=data[d]['scClass']
                sc.scPlayer1=p1
                sc.scPlayer2=p2
                sc.scPlayer1Name=p1.pyName
                sc.scPlayer1Rank=p1.pyRank
                sc.scPlayer2Name=p2.pyName
                sc.scPlayer2Rank=p2.pyRank
                sc.scTimeBreak=not follow_time
                sc.scDraft = True

                if 'Final' in request.POST.get('action'):
                    sc.scDraft = False
                sc.save()

        return render(request, 'squash_draw/success.html')
    
    except Exception as e:
        print(e)
        return render(request, 'squash_draw/fail.html')
            
         
def drawmatch_backend(request):
    """
    View of the backend got from the drawmatch interface
    """

    try:
        # get value from form
        schedule_pattern = request.POST.get('pattern')
        schedule_order = request.POST.get('order')
        schedule_date = request.POST.get('date')

        # generate schedule
        schedule = generate_schedule( schedule_pattern, schedule_order, schedule_date )
        for junior_match in schedule[0]:
            match = Schedule( scDate= convert_date( junior_match['match_date'] ), scTime=junior_match['match_time'], scClass=junior_match['match_class'],
                                scPlayer1=junior_match['player1'], scPlayer2=junior_match['player2'], scTimeBreak=junior_match['time_break'],
                                scPlayer1Name=junior_match['player1'].pyName, scPlayer1Rank=junior_match['player1'].pyRank,
                                scPlayer2Name=junior_match['player2'].pyName, scPlayer2Rank=junior_match['player2'].pyRank )
            match.save()

        for senior_match in schedule[1]:
            match = Schedule( scDate= convert_date( senior_match['match_date'] ), scTime=senior_match['match_time'], scClass=senior_match['match_class'],
                                scPlayer1=senior_match['player1'], scPlayer2=senior_match['player2'], scTimeBreak=senior_match['time_break'],
                                scPlayer1Name=senior_match['player1'].pyName, scPlayer1Rank=senior_match['player1'].pyRank,
                                scPlayer2Name=senior_match['player2'].pyName, scPlayer2Rank=senior_match['player2'].pyRank)
            match.save()

        # get date of draw from POST or GET
        match_date = schedule_date

        # get matches info from database
        matches = Schedule.objects.filter( scDate=convert_date(match_date) ).exclude( scPlayer1 = None, scPlayer2 = None ).order_by( 'scTime' )

        # create context dictionary
        match_list = []
        draft = False
        for m in matches:
            if m.scDraft:
                draft=True
            match_list.append({
                'date':m.scDate.strftime("%d/%m/%Y"), 
                'time':m.scTime.strftime('%H:%M'), 
                'class':m.scClass,
                'player1': m.scPlayer1.id,
                'player2': m.scPlayer2.id,
                'time_break': m.scTimeBreak,
                'id':m.id
            })
        
        # get players
        players = Player.objects.all()
        player_list = []
        for p in players:
            player_list.append({
                'id':p.id,
                'name':p.pyName
            })
        
        context = {'matches':match_list, 'players':player_list, 'draft':draft}

        return render(request, 'squash_draw/edit_schedule.html', context)

    except Exception as e:
        print(e)
        return render(request, 'squash_draw/fail.html')

def delete_match(request):
    """
    This view is to delete match
    """

    try:

        # get id
        id = request.GET.get('id')

        # get date from match
        sc = Schedule.objects.filter(id=id)[0]
        date = sc.scDate

        # delete match
        sc.delete()
    
        match_date = date.strftime("%d/%m/%Y")

        # get matches info from database
        matches = Schedule.objects.filter( scDate=convert_date(match_date) ).exclude( scPlayer1 = None, scPlayer2 = None ).order_by( 'scTime' )

        # create context dictionary
        match_list = []
        draft = False
        for m in matches:
            if m.scDraft:
                draft=True
            match_list.append({
                'date':m.scDate.strftime("%d/%m/%Y"), 
                'time':m.scTime.strftime('%H:%M'), 
                'class':m.scClass,
                'player1': m.scPlayer1.id,
                'player2': m.scPlayer2.id,
                'time_break': m.scTimeBreak,
                'id':m.id
            })
        
        # get players
        players = Player.objects.all()
        player_list = []
        for p in players:
            player_list.append({
                'id':p.id,
                'name':p.pyName
            })
        
        context = {'matches':match_list, 'players':player_list, 'draft':draft}

        return render(request, 'squash_draw/edit_schedule.html', context)

    except Exception as e:
        print(e)
        return render(request, 'squash_draw/fail.html')

def delete_match_enter_score(request):
    """
    This view is to delete match
    """

    try:

        # get id
        id = request.GET.get('id')

        # get date from match
        sc = Schedule.objects.filter(id=id)[0]

        # delete match
        sc.delete()
    
        # get schedule information0
        sc_obj_list = Schedule.objects.filter(scDraft = "False").order_by( 'scDate', 'scTime' )

        # create dictionary for schedule
        schedule_list = []
        for sc in sc_obj_list:
            
            schedule_list.append({ 
                'date':sc.scDate.strftime("%d/%m/%Y"), 
                'time':sc.scTime.strftime("%I:%M %p"), 
                'class':sc.scClass,
                'player1_name': sc.scPlayer1Name, 
                'player1_rank': sc.scPlayer1Rank,
                'player1_score': sc.scPlayer1Score,
                'player2_name': sc.scPlayer2Name, 
                'player2_rank': sc.scPlayer1Rank,
                'player2_score': sc.scPlayer2Score,
                'time_break': sc.scTimeBreak,
                'id': sc.id 
            })

        context = {'schedule':schedule_list}
        return render(request, 'squash_draw/record_score.html', context)

    except Exception as e:
        print(e)
        return render(request, 'squash_draw/fail.html')

def list_draw(request):

    # get distinct date from draw
    date_obj_list = Schedule.objects.order_by('scDate').values_list('scDate').distinct()
    date_list = [ d[0].strftime( '%d/%m/%Y' ) for d in date_obj_list ]
    
    # create context
    context = {}
    draw_list = []
    for d in date_obj_list:
        # get match in that date
        matches = Schedule.objects.filter( scDate = d[0] )

        # get only 1 match
        m = matches[0]

        # get status of draw
        draw_status = m.scDraft

        draw_list.append({
            'date': d[0].strftime( '%d/%m/%Y' ),
            'status':draw_status
        })

    context['draws'] = draw_list
    
    return render(request, 'squash_draw/list_draw.html', context)

def view_schedule(request):
    """
    This view is to display schedule in the table form
    """

    # get date from post or get
    match_date = request.GET.get('date') or request.POST.get('date')

    # get matches info from database
    j_matches = Schedule.objects.filter( scDate=convert_date(match_date), scClass="Juniors" ).exclude( scPlayer1 = None, scPlayer2 = None ).order_by( 'scTime' )
    s_matches = Schedule.objects.filter( scDate=convert_date(match_date), scClass="Seniors" ).exclude( scPlayer1 = None, scPlayer2 = None ).order_by( 'scTime' )

    # generate schedule
    schedule_list = []
    for s in s_matches:
        schedule_list.append({ 
            'date':s.scDate.strftime("%d/%m/%Y"), 
            'time':s.scTime.strftime('%H:%M'),
            'player1_name': s.scPlayer1.pyName, 
            'player1_rank': s.scPlayer1.pyRank,
            'player2_name': s.scPlayer2.pyName, 
            'player2_rank': s.scPlayer2.pyRank,
            'time_break': s.scTimeBreak
        })
    
    for j in j_matches:
        schedule_list.append({ 
            'date':j.scDate.strftime("%d/%m/%Y"), 
            'time':j.scTime.strftime('%H:%M'),
            'player1_name': j.scPlayer1.pyName, 
            'player1_rank': j.scPlayer1.pyRank,
            'player2_name': j.scPlayer2.pyName, 
            'player2_rank': j.scPlayer2.pyRank,
            'time_break': j.scTimeBreak
        })
        
    context = {'schedule':schedule_list}
    return render(request, 'squash_draw/view_schedule.html', context)

def delete_schedule(request):
    """
    This view is to display schedule in the table form
    """

    try:
        # get date from post or get
        match_date = request.GET.get('date') or request.POST.get('date')

        # get all matches
        matches = Schedule.objects.filter( scDate = convert_date(match_date))

        # delete all matches
        for m in matches:
            m.delete()

        return render(request, 'squash_draw/success.html')
    
    except Exception as e:
        print(e)
        return render(request, 'squash_draw/fail.html')

def edit_match_enter_score(request):
    """
    This view is used to edit the match for the enter score page
    """
    
    # get match id
    match_id = request.GET.get('id')

    # get match data from id
    match = Schedule.objects.filter(id=match_id)[0]

    # create context
    mdate = match.scDate.strftime("%d/%m/%Y") 
    mtime = match.scTime.strftime("%I:%M %p")
    mp1 = match.scPlayer1.id
    mp2 = match.scPlayer2.id
    mid = match.id

     # get players
    players = Player.objects.all()
    player_list = []
    for p in players:
        player_list.append({
            'id':p.id,
            'name':p.pyName
        })
 
    context = {'date':mdate, 'time':mtime, 'mp1':mp1, 'mp2':mp2, 'mid':mid, 'players':player_list}
    return render(request, 'squash_draw/edit_match_enter_score.html', context)

def edit_match_enter_score_backend(request):
    """
    This view is used to edit the match for the enter score page as backend
    """
    
    try:
         # get match id
        match_id = request.POST.get('id')

        # get match data from id
        match = Schedule.objects.filter(id=match_id)[0]

        # query player information
        p1 = Player.objects.filter(id=request.POST.get('scPlayer1'))[0]
        p1_timelower = p1.pyTimeMustGreater
        p1_timeupper = p1.pyTimeMustLower

        p2 = Player.objects.filter(id=request.POST.get('scPlayer2'))[0]
        p2_timelower = p2.pyTimeMustGreater
        p2_timeupper = p2.pyTimeMustLower

        follow_time = False
        m_time = datetime.strptime( request.POST.get('scTime'), '%H:%M' ).time()
        if ( p1_timelower != datetime.strptime('00:00','%H:%M') or m_time >= p1_timelower ) and \
            ( p1_timeupper != datetime.strptime('00:00','%H:%M')  or m_time <= p1_timeupper ) and \
            ( p2_timelower != datetime.strptime('00:00','%H:%M') or m_time >= p2_timelower ) and \
            ( p2_timeupper != datetime.strptime('00:00','%H:%M')  or m_time <= p2_timeupper ):
            follow_time = True


        # edit
        match.scDate = convert_date(request.POST.get('scDate'))
        match.scTime = m_time
        match.scPlayer1 = p1 
        match.scPlayer2 = p2
        match.scPlayer1Name = p1.pyName,
        match.scPlayer1Rank = p1.pyRank,
        match.scPlayer2Name = p2.pyName,
        match.scPlayer2Rank = p2.pyRank,
        match.scTimeBreak= not follow_time

        match.save()

        # get schedule information0
        sc_obj_list = Schedule.objects.filter(scDraft = "False").order_by( 'scDate', 'scTime' )

        # create dictionary for schedule
        schedule_list = []
        for sc in sc_obj_list:
            schedule_list.append({ 
                'date':sc.scDate.strftime("%d/%m/%Y"), 
                'time':sc.scTime.strftime("%I:%M %p"), 
                'class':sc.scClass,
                'player1_name': sc.scPlayer1Name, 
                'player1_rank': sc.scPlayer1Rank,
                'player1_score': sc.scPlayer1Score,
                'player2_name': sc.scPlayer2Name, 
                'player2_rank': sc.scPlayer2Rank,
                'player2_score': sc.scPlayer2Score,
                'time_break': sc.scTimeBreak,
                'id': sc.id 
            })

        context = {'schedule':schedule_list}
        return render(request, 'squash_draw/record_score.html', context)

    except Exception as e:
        print(e)
        return render(request, 'squash_draw/fail.html')