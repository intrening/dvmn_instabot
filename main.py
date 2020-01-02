import os
import re
from dotenv import load_dotenv
from instabot import Bot
from pprint import pprint
import argparse


def is_user_exist(insta_bot, user_name):
    if insta_bot.get_user_id_from_username(user_name):
        return True
    return False


def get_mentioned_users(comment):
    pattern = r'(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)'
    return re.findall(
        pattern=pattern,
        string=comment['text'],
    )


def is_one_of_users_real(insta_bot, users):
    for user in users:
        if is_user_exist(insta_bot, user):
            return True
    return False


if __name__ == "__main__":
    load_dotenv()
    INSTA_LOGIN = os.getenv("INSTA_LOGIN")
    INSTA_PASSWORD = os.getenv("INSTA_PASSWORD")

    parser = argparse.ArgumentParser()
    parser.add_argument("media_link")
    parser.add_argument("media_author")
    args = parser.parse_args()
    media_link = args.media_link
    media_author = args.media_author

    insta_bot = Bot()
    insta_bot.login(username=INSTA_LOGIN, password=INSTA_PASSWORD)

    media_id = insta_bot.get_media_id_from_link(media_link)
    media_author_id = insta_bot.get_user_id_from_username(media_author)
    author_followers = insta_bot.get_user_followers(media_author_id)
    media_comments = insta_bot.get_media_comments_all(media_id)
    media_likers = insta_bot.get_media_likers(media_id)

    accepted_comments = []
    for comment in media_comments:
        comment_author_id = str(comment['user_id'])
        mentioned_users = get_mentioned_users(comment)
        if comment_author_id in media_likers and comment_author_id in author_followers:
            if is_one_of_users_real(insta_bot=insta_bot, users=mentioned_users):
                accepted_comments.append(comment)

    accepted_users = set([comment['user_id'] for comment in accepted_comments])
    pprint(accepted_users)
