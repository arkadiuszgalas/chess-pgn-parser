from datetime import datetime
from zoneinfo import ZoneInfo

# Function selects value for given tag from .pgn file
def get_tag_from_pgn(input_list,tag):
   tag_value = ''
   for i in range(len(input_list)):
      if input_list[i].find(tag) != -1:
          a = input_list[i].find('"')
          b = input_list[i][a + 1:].find('"')
          tag_value = input_list[i][a + 1:a + b + 1]
   return tag_value

# Function coverts date and hour strings into datetime format with GMT+0000 timezone
def convert_to_datetime(date_str, hour_str):
   hour_str_one = hour_str.find(":")
   hours_end_time = hour_str[0:hour_str_one]
   minutes_end_time = hour_str[hour_str_one + 1:hour_str_one + 3]
   seconds_end_time = hour_str[hour_str_one + 4:hour_str_one + 6]

   dt_converted = datetime(int(date_str[0:4]), int(date_str[5:7]), int(date_str[8:]),
                           int(hours_end_time), int(minutes_end_time), int(seconds_end_time), tzinfo=ZoneInfo('UTC'))
   return dt_converted

# Function calculates number of moves for white and black player
def find_number_of_moves(input_list_with_pgn):
   found_first_move = False
   j = 0
   num = 0
   while not found_first_move:
      if input_list_with_pgn[j].find("1. ") != -1:
         found_first_move = True
         num = j
      else:
         j = j + 1
   full_game_str = ''
   for k in range(num, len(input_list_with_pgn)):
      full_game_str += str(input_list_with_pgn[k])

   l = 2
   max_move_found = False
   while not max_move_found:
      l_str = str(l) + "."
      if full_game_str.find(l_str) != -1:
         l = l + 1
      else:
         max_move_found = True
         l = l - 1
   moves_w = l
   last_move = full_game_str[full_game_str.find(str(l) + ".") :]
   if last_move.find(" ") != -1:
      last_move_one = last_move[last_move.find(" ") + 1 :]
      if last_move_one.find(" ") != -1:
         last_move_sec = last_move_one[last_move_one.find(" ") + 1 :]
         if last_move_sec.find(" ") != -1:
            moves_b = l
         else:
            moves_b = l - 1
      else:
         moves_b = l - 1
   else:
      moves_b = l - 1
   moves_w_b = [moves_w, moves_b]
   return moves_w_b

# Function calculates how much time was used during game basic time
def calculate_used_basic_time(timecontrol,time_left):
   if timecontrol.find("+") != -1:
      plus_sign = timecontrol.find("+")
      basic_time = int(timecontrol[:plus_sign])
   else:
      basic_time = int(timecontrol)
   if time_left.find(":") != -1:
      white_first_sep = time_left.find(":")
      if time_left[white_first_sep + 1:].find(":") != -1:
         white_sec_sep = time_left[white_first_sep + 1:].find(":")
         hour_w = int(time_left[:white_first_sep])
         min_w = int(time_left[white_first_sep + 1:white_first_sep + white_sec_sep + 1])
         sec_w = int(time_left[white_first_sep + white_sec_sep + 2:])
      else:
         hour_w = 0
         min_w = int(time_left[:white_first_sep])
         sec_w = int(time_left[white_first_sep + 1:])
   else:
      print('Case 3: ')
      hour_w = 0
      min_w = 0
      sec_w = int(time_left)
      print('Seconds left' + str(time_left))
   time_used = basic_time - 3600 * hour_w - 60 * min_w - sec_w
   return time_used

# Function calculates how much time was added during increments
def calculate_used_increment_time(timecontrol, moves_number):
   if timecontrol.find("+") != -1:
      plus_sign = timecontrol.find("+")
      increment_value = int(timecontrol[plus_sign:])
   else:
      increment_value = 0
   time_added = moves_number * increment_value
   return time_added

# Function returns "white" if white wins, "black" if black wins or "draw"
def get_result(pgn_list):
   game_result = get_tag_from_pgn(pgn_list, "Result")
   if game_result == "1-0":
      final_result = "white"
   elif game_result == "0-1":
      final_result = "black"
   else:
      final_result = "draw"
   return final_result

# Function calculates line number in .pgn file where chess game score begins
def calculate_begin_line(pgn_list):
   i = 0
   first_move_found = False
   begin_line = 0
   while not first_move_found:
      if pgn_list[i].find("1. ") != -1:
         begin_line = i
         first_move_found = True
      i = i + 1
   return begin_line

# Function creates list composed of single chess moves
def create_list_with_single_moves(pgn_list, begin_line, number_moves):
   full_game_string = ''
   list_single_moves = []
   for i in range(begin_line, len(pgn_list)):
      full_game_string = full_game_string + str(pgn_list[i])

   for i in range(1, number_moves + 1):
      if i < number_moves:
         move_start = full_game_string.index(str(i) + '.')
         move_end = full_game_string.index(str(i + 1) + '.')
         move = full_game_string[move_start:move_end]
         list_single_moves.append(move)
      else:
         move_start = full_game_string.index(str(i) + '.')
         move = full_game_string[move_start:]
         list_single_moves.append(move)
   return list_single_moves
