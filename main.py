from datetime import timedelta
from pathlib import Path
from functions_parser import *

# Calculate type of game, is it: rapid, blitz, bullet
def get_game_time(timecontrol_string):
   if timecontrol_string.find('+') != -1:
      main_part = timecontrol_string[:timecontrol_string.find('+')]
      increment_part = timecontrol_string[timecontrol_string.find('+') + 1:]
      game_time = int(main_part) + 60 * int(increment_part)
   else:
      game_time = int(timecontrol_string)
   if game_time < 180 or timecontrol_string == '120+1':
      game_t = 'bullet'
   elif game_time < 600 or timecontrol_string == '300+5':
      game_t = 'blitz'
   else:
      game_t = 'rapid'
   return game_t

def get_maximum_prefix(output_path):
   p = Path(output_path)
   list_pgn = list(p.glob('*.pgn'))
   max_found = 0
   if len(list_pgn) == 0:
      prefix = '0001'
   else:
      for i in range(len(list_pgn)):
         if int(str(list_pgn[i].name)[0:4]) > max_found:
            max_found = int(str(list_pgn[i].name)[0:4])
      prefix = str(max_found + 1).zfill(4)
   return prefix
white_left = input('How much time while player has left: (hh:mi:ss) \n')
black_left = input('How much time black player has left: (hh:mi:ss) \n')

input_dir = Path.cwd() / 'input'
# Create list of pgn files within input directory
# Current version's assumption is there is only one .pgn file in input directory
input_files = list(input_dir.glob('*.pgn'))

input_pgn_file = open(input_files[0], "r", encoding = "utf8")
input_pgn_data =  input_pgn_file.read()
input_pgn_list = input_pgn_data.split("\n")
input_pgn_file.close()

timecontrol = get_tag_from_pgn(input_pgn_list,"TimeControl")

game_type = get_game_time(timecontrol)

# Check if output directory exists, if not create it
output_dir = Path.cwd() / 'output/' / game_type
if not output_dir.exists():
   output_dir.mkdir()
   file_prefix = '0001'
else:
   file_prefix = get_maximum_prefix(output_dir)

# Getting white player name and black player name
w_player = get_tag_from_pgn(input_pgn_list, "White ")
b_player = get_tag_from_pgn(input_pgn_list, "Black ")

# Getting date and endtime of game
date_game = get_tag_from_pgn(input_pgn_list, "Date")
endtime_game = get_tag_from_pgn(input_pgn_list, "EndTime")

# Convert date and time values to UTC timezone
dt_end = convert_to_datetime(date_game, endtime_game)

# Calculating number of moves for white and black
num_moves = find_number_of_moves(input_pgn_list)
print(str(num_moves))

# Calculate basic time for white player
w_basic_time_used = calculate_used_basic_time(timecontrol, white_left)
print('Basic time used for white player: ' + str(w_basic_time_used))
# Calculate basic time for black player
b_basic_time_used = calculate_used_basic_time(timecontrol, black_left)
print('Basic time used for black player: ' + str(b_basic_time_used))
# Calculate used increment time (added) for white player

# Calculate added time for white player
w_increment_time_added = calculate_used_increment_time(timecontrol, num_moves[0])
print("Added time for white: " + str(w_increment_time_added))

# Calculate added time for black player
b_increment_time_added = calculate_used_increment_time(timecontrol, num_moves[1])
print("Added time for black: " + str(b_increment_time_added))

# Calculate total used time - basic and added
wb_total_used_time = w_basic_time_used + b_basic_time_used + w_increment_time_added + b_increment_time_added
print("Total calculated time of game: " + str(wb_total_used_time))

# Calculate game begin time and convert it to specific timezone
dt_begin = dt_end - timedelta(seconds = wb_total_used_time)
dt_begin_converted = dt_begin.astimezone(ZoneInfo('Europe/Warsaw'))
print("Begin game: " + str(dt_begin_converted))

# Select ECO code tag from .pgn file
eco_code = get_tag_from_pgn(input_pgn_list, "ECO")
# Select result from "Result" tag within .pgn
fin_result = get_result(input_pgn_list)
print("Result:" + str(fin_result))

# Building output filename
year_fn = dt_begin_converted.strftime("%Y")
month_fn = dt_begin_converted.strftime("%m")
day_fn = dt_begin_converted.strftime("%d")
hour_fn = dt_begin_converted.strftime("%H")
minute_fn = dt_begin_converted.strftime("%M")
second_fn = dt_begin_converted.strftime("%S")

output_filename = file_prefix + "_" + year_fn + month_fn + day_fn + "_" + hour_fn + minute_fn + second_fn + "_" + w_player + "_" + b_player + "_" + eco_code + "_" + fin_result + ".pgn"
print("Output filename: " + output_filename)

# Calculate line where chess game scores begins within .pgn file
start_line = calculate_begin_line(input_pgn_list)
print("Begin line: " + str(start_line))

# Create list composed of single moves
single_moves_list = create_list_with_single_moves(input_pgn_list, start_line, num_moves[0])

# Save information to output file
output_file = output_dir / output_filename
f = open(output_file, "w", encoding ="utf8")
for j in range(start_line):
   f.write(input_pgn_list[j] + "\n")
for j in range(len(single_moves_list)):
   f.write(single_moves_list[j] + "\n")
f.close()