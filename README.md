# NBA_Player_Stats

Displays the NBA player stats based on the player user inputs

If the user wants to see the career stats for the NBA player then input
the player alone

If the user wants to see the season stats for the NBA player then input the 
player and the season.

# Installation

pip install requests

pip install pandas

pip install flask

pip install twilio

# Run

To run on your phone you must have a Twilio account and create a phone number
change the name in Flask to your account. Run 'python NBA_SMS.py' in your terminal
start a tunnel 'ngrok http 5000' on your other terminal. Copy the last url and past 
it to your Twilio phone number console add '/sms' to the end of the route and save.
You can then input a 'Lebron James' or 'Lebron James 2012' and you'll see the stats.

If you don't want to do this via SMS and just to the command line, then run 'python Carrer_Season.py'
and the command line version will do the same. 
