# chess-pgn-parser
# Ideas for improvements:
1. Adding to configuration source directory. Now: hard coded source directory Path.cwd() / 'input' (current_directory/input).
2. Adding to configuration target directory. Now: hard coded source directory Path.cwd() / 'output/' / game_type.
3. Adding option to delete source file(-s).
4. Changing output directory to output/rapid/yyyy/mm. Now: output/rapid
5. Adding timezone to configuration. Now: timezone is hard coded as 'Europe/Warsaw'
6. Adding the ability to parse multiple .pgn file at once
7. Improved .pgn file parsing: removing trailing spaces from each move
8. Improved .pgn file parsing: adding leading space for moves 1,2,..,9

# Known errors:
None