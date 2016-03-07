team = 'Sabres' # Select the team you want
# Avalanche, Blackhawks, Blue Jackets, Blues, Bruins, Canadiens, Canucks, Capitals, Coyotes, Devils, Ducks, Flames, Flyers, Hurricanes, Islanders, Jets, Kings, Lightning, Maple Leafs ,Oilers, Panthers, Penguins, Predators, Red Wings, Sabres, Senators, Sharks, Stars, Wild


from colorama import init, Fore, Style
import datetime
import json
import os
import platform
import sys
import time
import requests
import RPi.GPIO as GPIO
import socket 

i = datetime.datetime.now()  # date and time formatting http://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT) #Set the Raspberry Pi GPIO pin 7 as output

refresh_time = 21600  # 6 hours Refresh time (seconds), NHL API refresh is every 60 seconds
api_url = 'http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp?loadScoreboard=jQuery110105207217424176633_1428694268811&_=1428694268812'
api_headers = {'Host': 'live.nhle.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', 'Referer': 'http://www.nhl.com/ice/scores.htm'}

#Home team variables
old_score = 0

team_playing = False

#Away team variables
away_old_score = 0


show_today_only = False


def main():
	global refresh_time
	global team
	global team_playing
	global old_score
	global away_old_score
	clear_screen()
	
	# Format dates to match NHL API style:
	
	# Todays date
	t = datetime.datetime.now()
	todays_date = "" + t.strftime("%A") + " " + "%s/%s" % (t.month, t.day)
	
	# Yesterdays date
	y =y = t - datetime.timedelta(days=1)
	yesterdays_date = "" + y.strftime("%A") + " " + "%s/%s" % (y.month, y.day)
	
	while True:
				
			try:
				r = requests.get(api_url, headers=api_headers) #making sure there is a connection with the API
			except (requests.ConnectionError): #Catch these errors
				print ("Could not get response from NHL.com trying again...")
				time.sleep(5)
				continue
			except(requests.HTTPError):
				print ("HTTP Error when loading url. Please restart program. ")
				sys.exit(0)
			except(requests.Timeout):
				print ("The request took too long to process and timed out. Trying again... ")
				time.sleep(5)
			except(socket.error):
				print ("Could not get response from NHL.com trying again...")
				time.sleep(5)
			except(requests.RequestException):
				print ("Unknown error. Please restart the program. ")
				sys.exit(0)
			
			
			# We get back JSON data with some JS around it, gotta remove the JS
			json_data = r.text
			
			# Remove the leading JS
			json_data = json_data.replace('loadScoreboard(', '')
			
			# Remove the trailing ')'
			json_data  = json_data[:-1]
			
			data = json.loads(json_data)
			for key in data:
				if key == 'games':
					for game_info in data[key]:
					
						# Assign more meaningful names
						game_clock = game_info['ts']
						game_stage = game_info['tsc']
						status = game_info['bs']
						
						away_team_locale = game_info['atn']
						away_team_name = game_info['atv'].title()
						away_team_score = game_info['ats']
						away_team_result = game_info['atc']
						
						
						home_team_locale = game_info['htn']
						home_team_name = game_info['htv'].title()
						home_team_score = game_info['hts']
						home_team_result = game_info['htc']
						
						# Fix strange names / locales returned by NHL
						away_team_locale = fix_locale(away_team_locale)
						home_team_locale = fix_locale(home_team_locale)
						away_team_name = fix_name(away_team_name)
						home_team_name = fix_name(home_team_name)
						
						
						
						
						
						# Show games from Yesterday and today or just today
						if (yesterdays_date in game_clock.title() and not show_today_only) or todays_date in game_clock.title() or 'TODAY' in game_clock or 'LIVE' in status:
						
							header_text = away_team_locale + ' ' + away_team_name + ' @ ' + home_team_locale + ' ' + home_team_name
							
							# Different displays for different states of game:
							# Game from yesterday, ex: on YESTERDAY, MONDAY 4/20 (FINAL 2nd OT)
							# Game from today finished, ex: TODAY (FINAL 2nd OT)
							if 'FINAL' in status:
								if yesterdays_date in game_clock.title():
									header_text += '\nYESTERDAY, ' + game_clock + ' '
								elif todays_date in game_clock.title() or 'TODAY' in game_clock:
									header_text += '\nTODAY '
								header_text += '(' + status + ')'
							
							
							
							
							# Upcoming game, ex: TUESDAY 4/21, 7:00 PM EST)
							elif 'DAY' in game_clock:
								header_text += Fore.YELLOW + '\n(' + game_clock + ', ' + status + ' EST)' + Fore.RESET
							
							# Last 5 minutes of game and overtime, ex: (1:59 3rd PERIOD) *in red font*
							elif 'critical' in game_stage:
								header_text += '\n(' + Fore.RED + game_clock + ' PERIOD' + Fore.RESET + ')'
							
							
							# Any other time in game, ex: (10:34 1st PERIOD)
							else:
								header_text += Fore.YELLOW + '\n(' + game_clock + ' PERIOD)' + Style.RESET_ALL
							
							
							print(header_text)
							
							
							
							
							
							# Highlight the winner of finished games in green, and games underway in blue:
							# Away team wins
							if away_team_result == 'winner':
								print(Style.BRIGHT + Fore.GREEN + away_team_name + ': ' + away_team_score + Style.RESET_ALL)
								print(home_team_name + ': ' + home_team_score)
							
							
							# Home team wins
							elif home_team_result == 'winner':
								print(away_team_name + ': ' + away_team_score)
								print(Style.BRIGHT + Fore.GREEN + home_team_name + ': ' + home_team_score + Style.RESET_ALL)
							
							
							# Game still underway
							elif 'progress' in game_stage or 'critical' in game_stage:
								print(Fore.CYAN + away_team_name + ': ' + away_team_score)
								print(home_team_name + ': ' + home_team_score + Fore.RESET)
								game_home(home_team_name,home_team_score,game_clock,status) 
								game_away(away_team_name,away_team_score,game_clock,status)
							
															
							# Game hasn't yet started
							else:
								print(away_team_name + ': ' + away_team_score)
								print(home_team_name + ': ' + home_team_score)
								game_home(home_team_name,home_team_score,game_clock,status)
								game_away(away_team_name,away_team_score,game_clock,status)
							print('')
							if ('FINAL' in status) and (away_team_name == team or home_team_name == team) and (yesterdays_date in game_clock.title() or todays_date in game_clock.title() ): #Game over, no need to refresh every minute
								print "Game over!"
								refresh_time = 21600
								team_playing = False
								old_score = 0 
								away_old_score = 0
								print "Refresh in: " + str(refresh_time) + " seconds (6 hours)"
								print "Team playing: " + str(team_playing)
								print ""

							
							
							
							
							
			
			if team_playing == False:
				print ("Current time: " + str(datetime.datetime.now()))
				refresh_time = 21600 # 6 hours
				print team + " are not playing. Refreshing in " + str(refresh_time) + " seconds (6 hours)."
			# Perfrom the refresh
			time.sleep(refresh_time)

			
			
def clear_screen():
	if platform.system() == 'Windows':
		os.system('cls')
	else:
		os.system('clear')


def print_help():
	print('By default games from yesterday and today will be displayed.')
	print('')
	print('If you want to see games from just today run the program with ')
	print('the "--today-only" flag.')


def fix_locale(team_locale):
	# NHL API forces team name in locale for both New York teams, i.e. locale + name == "NY Islanders islanders"
	if 'NY ' in team_locale:
		return 'New York'
	
	if 'Montr' in team_locale:
		return 'Montreal'
	
	return team_locale




def game_away(away_team_name, away_team_score, game_clock, status):
	global refresh_time
	global away_old_score
	global team_playing
	current_time = time.strftime("%I:%M:%S")
	game_time = str(status)
	game_date = game_clock
	now = datetime.datetime.now()
	now_second = now.second
	
	if team in away_team_name:
		print""
		print""
		print ("Current time: " + current_time) 
		team_playing = True
		
		if (game_date != "TODAY" and game_time != "LIVE"):
			print("Game time is quite aways away!")
			refresh_time = 21600 # 6 hours
			away_old_score = 0
			print "Refreh time: " + str(refresh_time) + " seconds (6 hours)"
			print "Away old_score: " + str(away_old_score)
		
		
		elif (game_date == "TODAY"): #Game time is near
			refresh_time = 3600 # 1 hours
			print "It is game day!"
			print "Refresh time is : " + str(refresh_time) + " seconds (1 hour)"
		
		
		elif (game_date == "PRE GAME"): #30 minutes to game time
			refresh_time = 300 # 5 minutes
			print "It is almost game time!"
			print "Refresh time: " + str(refresh_time) + " seconds (5 minutes)"
		
		
		else: # Game is underway
			#The API url refreshes at exactly the next minute. So we calculate the time until the next minute, set it to refresh then
			refresh_time = 63 - now.second - now.microsecond/1e6
			print "Refresh time: " + str(refresh_time) + " seconds"
			print "Away old_score: " + str(away_old_score)
			
			
			if int(away_old_score) < int(away_team_score): # If the old score < the new score, a goal was scored
				print team + " have scored a goal!"
				GPIO.output(7, True) # Activate the light
				time.sleep(1)
				GPIO.output(7, False) # Turn the rPI pin off so we can use it again
				away_old_score = int(away_team_score) # Set the old_score to be the current score
				print "Away old_score: " + str(away_old_score)
				
	elif team_playing == False: # The selected team isn't playing
		refresh_time = 21600 # 6 hours
		away_old_score = 0
		print "Away old_score: " + str(away_old_score)
		print "Not " + team + " gameday!! Refresh in: " + str(refresh_time) + " seconds (6 hours)"






def game_home(home_team_name, home_team_score, game_clock, status):
	global refresh_time
	global old_score
	global team_playing
	current_time = time.strftime("%I:%M:%S")
	game_time = str(status)
	game_date = game_clock
	now = datetime.datetime.now()
	now_second = now.second	
	
	if team in home_team_name:
		print""
		print""
		print ("Current time: " + current_time) 
		team_playing = True
		
		if (game_date != "TODAY" and game_time != "LIVE"):
			print("Game time is quite aways away!")
			refresh_time = 21600 # 6 hours
			old_score = 0
			print "Refreh time: " + str(refresh_time) + " seconds (6 hours)"
			print "Home old_score: " + str(old_score)
		
		
		elif (game_date == "TODAY"): #Game time is near
			refresh_time = 3600 # 1 hours
			print "It is game day!"
			print "Refresh time is : " + str(refresh_time) + " seconds (1 hour)"
		
		
		elif (game_date == "PRE GAME"): #30 minutes to game time
			refresh_time = 300 # 5 minutes
			print "It is almost game time!"
			print "Refresh time: " + str(refresh_time) + " seconds (5 minutes)"
		
		
		else: # Game is underway
			print "Now: " + str(now)
			print "Now.second: " + str(now_second)
			
			#The API url refreshes at exactly the next minute. So we calculate the time until the next minute, set it to refresh then
			refresh_time = 63 - now.second - now.microsecond/1e6
			print "Time untill next minute: " + str(refresh_time)
			print "Refresh time: " + str(refresh_time) + " seconds"
			print "Home old_score: " + str(old_score)
			
			
			if int(old_score) < int(home_team_score): # If the old score < the new score, a goal was scored
				print team + " have scored a goal!"
				GPIO.output(7, True) # Activate the light
				time.sleep(1)
				GPIO.output(7, False) # Turn the rPI pin off so we can use it again
				old_score = int(home_team_score) # Set the old_score to be the current score
				print "Home old_score: " + str(old_score)
				
	elif team_playing == False: # The selected team isn't playing
		refresh_time = 21600 # 6 hours
		old_score = 0
		print "Home old_score: " + str(old_score)
		print "Not " + team + " gameday!! Refresh in: " + str(refresh_time) + " seconds (6 hours)"






def fix_name(team_name):
	#Change 'redwings' to 'Red Wings'
	if 'wings' in team_name:
		return 'Red Wings'
	
	if 'jackets' in team_name:
		return 'Blue Jackets'
	
	if 'leafs' in team_name:
		return 'Maple Leafs'
	
	return team_name



def parse_arguments(arguments):
	global show_today_only
	for x in range(1, len(arguments)):
		argument = arguments[x]
		
		if argument == '--help' or argument == '-h':
			print_help()
			sys.exit(0)
		elif argument == '--today-only':
			show_today_only = True




if __name__ == '__main__':
    # Initialize Colorama
    init()

    # Parse any arguments provided
    parse_arguments(sys.argv)

    # Start the main loop
    main()
