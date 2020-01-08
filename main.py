import os
import re
from dotenv import load_dotenv
from instabot import Bot
from pprint import pprint
import argparse


def is_user_exist(insta_bot, user_name):
    return insta_bot.get_user_id_from_username(user_name)


def get_mentioned_users(comment):
    pattern = r'(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)'
    return re.findall(pattern=pattern, string=comment['text'])


def is_one_of_users_real(insta_bot, users):
    return any(is_user_exist(insta_bot, user) for user in users)


def main():
    load_dotenv()
    insta_login = os.getenv("INSTA_LOGIN")
    insta_password = os.getenv("INSTA_PASSWORD")

    parser = argparse.ArgumentParser()
    parser.add_argument("media_link")
    parser.add_argument("media_author")
    args = parser.parse_args()
    media_link = args.media_link
    media_author = args.media_author

    insta_bot = Bot()
    insta_bot.login(username=insta_login, password=insta_password)
    media_id = insta_bot.get_media_id_from_link(media_link)
    media_comments = insta_bot.get_media_comments_all(media_id)
    media_author_id = insta_bot.get_user_id_from_username(media_author)
    author_followers = set(insta_bot.get_user_followers(media_author_id))
    media_likers = set(insta_bot.get_media_likers(media_id))
    appropriate_users = author_followers & media_likers

    accepted_comments = []
    for comment in media_comments:
        comment_author_id = str(comment['user_id'])
        mentioned_users = get_mentioned_users(comment)
        if comment_author_id in appropriate_users and is_one_of_users_real(insta_bot=insta_bot, users=mentioned_users):
            accepted_comments.append(comment)

    accepted_users = set([comment['user_id'] for comment in accepted_comments])
    pprint(accepted_users)


if __name__ == "__main__":
    main()
