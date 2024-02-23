import json

from flask import Flask, request, redirect, url_for, render_template, g, Response

from fetch_user_posts import fetch_user_posts
from insert_tweet_to_db import insert_tweets_into_db
from login_and_save_cookies import login_and_save_cookies

app = Flask(__name__)

import asyncio
import os
from flask import Flask, send_file

async def main(username:str , password: str, user_to_scrape: str):
    if not os.path.exists('twitter_cookies.json'):
        await login_and_save_cookies(username, password)
    await fetch_user_posts(f'https://twitter.com/{user_to_scrape}')

    insert_tweets_into_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_to_scrape = request.form['username_to_scrape']

        asyncio.run(login_and_save_cookies(username, password))
        asyncio.run(main(username, password, user_to_scrape))
        return redirect(url_for('download_tweets'))
    else:
        return render_template('indexTweet.html', file_exists=os.path.exists('tweets_data.json'))


@app.route('/download-tweets')
def download_tweets():

    if os.path.exists('tweets_data.json'):
        return send_file('tweets_data.json', as_attachment=True)
    else:
        return 'File not found.', 404

@app.route('/create-user-profile', methods=['GET', 'POST'])
def create_user_profile():
    if request.method == 'POST':

        height = request.form['height']
        weight = request.form['weight']
        nutrition_goals = request.form.get('nutrition_goals', '')
        meal_preferences = request.form.get('meal_preferences', '')


        user_profile = {
            "height": height,
            "weight": weight,
            "nutrition_goals": nutrition_goals,
            "meal_preferences": meal_preferences
        }


        user_profile_json = json.dumps(user_profile, indent=4)


        response = Response(user_profile_json, mimetype='application/json')
        response.headers['Content-Disposition'] = 'attachment; filename=user_profile.json'
        return response
    else:

        return render_template('indexTweet.html')



if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run()
