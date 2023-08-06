#!/usr/bin/env python
# coding=utf-8

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import unittest
import pytest
import unittest.mock

from sopel_modules.lastfm import lastfm


def test_format_song_output():
    expected = '♫ user last listened to artist - song (album) ♫'
    out = lastfm.format_song_output('user', 'last listened to', 'artist',
                                    'song', 'album')

    assert expected == out


def test_get_api_url():
    expected = ('http://ws.audioscrobbler.com/2.0/'
                '?method=user.getrecenttracks'
                '&user=testuser&api_key=testkey'
                '&format=json&limit=1')
    out = lastfm.get_api_url('testuser', 'testkey')

    assert expected == out


def test_get_action_is_listening():
    expected = 'is listening to'

    last_track = {'@attr': {'nowplaying': 'true'}}
    out = lastfm.get_action(last_track)

    assert expected == out


def test_get_action_last_listened():
    expected = 'last listened to'

    last_track = {}
    out = lastfm.get_action(last_track)

    assert expected == out


def test_get_lastfm_user_with_arg():
    expected = 'arg_user'

    out = lastfm.get_lastfm_user('arg_user', 'nick', 'config')

    assert expected == out


@unittest.mock.patch('sopel_modules.lastfm.sopel.db.SopelDB')
def test_get_lastfm_user_from_db(mock_db):
    expected = 'db_user'

    mock_db.return_value.get_nick_value.return_value = 'db_user'

    out = lastfm.get_lastfm_user(None, 'nick', 'config')

    assert expected == out


@unittest.mock.patch('sopel_modules.lastfm.sopel.db.SopelDB')
def test_get_lastfm_user_none(mock_db):
    mock_db.return_value.get_nick_value.return_value = None

    with pytest.raises(lastfm.NoUserSetException) as e:
        lastfm.get_lastfm_user(None, 'nick', 'config')

    msg = 'User not set, use .fmset or pass user as argument'
    assert (str(e.value)) == msg


def test_get_last_track():
    expected = 'last track'

    json = {'recenttracks': {'track': ['last track']}}
    out = lastfm.get_last_track(json)

    assert expected == out


def test_get_last_track_no_user():
    with pytest.raises(lastfm.NoUserException) as e:
        lastfm.get_last_track({})
    assert str(e.value) == 'User not found'


def test_get_last_track_no_tracks():
    json = {'recenttracks': {'track': []}}
    with pytest.raises(lastfm.NoTracksException) as e:
        lastfm.get_last_track(json)
    assert str(e.value) == 'User has not listened to any tracks yet'
