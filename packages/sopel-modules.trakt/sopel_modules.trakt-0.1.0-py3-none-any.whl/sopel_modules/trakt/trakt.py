# coding=utf-8

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import os
import itertools
import random
import textwrap

import sopel.module
from sopel.config.types import StaticSection, ValidatedAttribute
import sopel.db
import requests


class TraktSection(StaticSection):
    api = ValidatedAttribute('api')


def setup(bot):
    bot.config.define_section('trakt', TraktSection)


def configure(config):
    config.define_section('trakt', traktSection, validate=False)
    config.trakt.configure_setting('api', 'Enter trakt api: ')


class NoUserSetException(Exception):
    pass


class NoUserException(Exception):
    pass


class NoHistoryException(Exception):
    pass


def format_episode_output(user, show, season, episode, title):
    pad_episode = str(episode).zfill(2)
    return f'{user} last watched: {show} {season}x{pad_episode} - {title}'


def format_movie_output(user, film, year):
    return f'{user} last watched: {film} ({year})'


def format_output(user, json):
    if json['type'] == 'episode':
        return format_episode_output(user,
                                     json['show']['title'],
                                     json['episode']['season'],
                                     json['episode']['number'],
                                     json['episode']['title'])
    if json['type'] == 'movie':
        return format_movie_output(user,
                                   json['movie']['title'],
                                   json['movie']['year'])


def get_trakt_user(arg, nick, config):
    if arg:
        return arg

    db = sopel.db.SopelDB(config)
    trakt_user = db.get_nick_value(nick, 'trakt_user')
    if trakt_user:
        return trakt_user

    msg = 'User not set, use .traktset or pass user as argument'
    raise NoUserSetException(msg)


def get_api_url(user):
    return f'https://api.trakt.tv/users/{user}/history'


def get_headers(api_key):
    return {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': api_key
    }


def get_last_play(response):
    if response.status_code == 404:
        raise NoUserException('User does not exist')

    if len(response.json()) == 0:
        raise NoHistoryException('User has no history')

    return response.json()[0]


@sopel.module.commands('trakt')
def trakt_command(bot, trigger):
    api_key = os.getenv('SOPEL_TRAKT_API') or bot.config.trakt.api
    if not api_key:
        bot.say('No api key set, set in config or environment variable')
        return

    try:
        user = get_trakt_user(trigger.group(2), trigger.nick, bot.config)
    except NoUserSetException as e:
        bot.say(str(e))
        return

    api_url = get_api_url(user)
    headers = get_headers(api_key)
    r = requests.get(api_url, headers=headers)

    try:
        last_play = get_last_play(r)
    except (NoUserException, NoHistoryException) as e:
        bot.say(str(e))
        return

    out = format_output(user, last_play)
    bot.say(out)


@sopel.module.commands('traktset')
def traktset(bot, trigger):
    user = trigger.group(2)

    if not user:
        bot.say('no user given')
        return

    db = sopel.db.SopelDB(bot.config)
    db.set_nick_value(trigger.nick, 'trakt_user', user)

    bot.say(f'{trigger.nick}\'s trakt user is now set as {user}')
