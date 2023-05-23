import logging
import requests
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define command handlers
def start(update, context):
    league_explanation = (
        "Enter the league code for the desired football league, you will get the top 5 teams in this league:\n"
        "CL: UEFA Champions League\n"
        "BL1: (Germany) Bundesliga\n"
        "DED: (Holland) Eredivisie\n"
        "BSA: (Brazil) Campeonato Brasileiro Série A\n"
        "PD: (Spain)Primera Division\n"
        "FL1: (France) Ligue 1\n"
        "PPL: (Portugal) Primeira Liga\n"
        "SA: (Italy) Serie A\n"
        "PL: (England) Premier League\n"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your football league bot.\nֿֿ" + league_explanation)

def get_top_teams(update, context):
    league_name = update.message.text.upper()
    # Make a request to the API
    response = requests.get(f"https://api.football-data.org/v2/competitions/{league_name}/standings", headers={"X-Auth-Token": "5320394cf404487082975218a485ce4a"})
    if response.status_code == 200:
        print("hello baby")
        data = response.json()
        standings = data['standings'][0]['table']

        top_teams = '\n'.join([f"{team['position']}. {team['team']['name']}" for team in standings[:5]])

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"The top 5 teams in {league_name} are:\n{top_teams}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to fetch league data. Please try again.")


if __name__ == '__main__':
    # Set up the bot
    # update_queue = Updater.update_queue
    # updater = Updater("6002567546:AAHouDGvyZdIUcwnWB4yXjMFoTuZLlGlcJg", use_context=True, update_queue=update_queue)
    updater = Updater("6002567546:AAHouDGvyZdIUcwnWB4yXjMFoTuZLlGlcJg", use_context=True)


    # Register command handlers
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, get_top_teams))

    # Start the bot
    updater.start_polling()


