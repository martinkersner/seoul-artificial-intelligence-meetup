# -*- coding: utf-8 -*-
import yaml
import meetup.api
import twitter
from slacker import Slacker
from pprint import pprint
import datetime
import re
import facebook
import argparse
from os import listdir
from os.path import isfile, join

epoch_now = int(datetime.datetime.now().strftime("%s")) * 1000

hosts = {
    'cinyoung': 203189175,
    'martin': 189944980,
    'adel': 201618648
}

with open("config.yml", 'r') as ymlfile:
  cfg = yaml.load(ymlfile)
key_dict = cfg['apikey']

# commands
FIRE = 'fire'
TEST = 'test'
PHOTO = 'photo'


def print_event(sns, msg):
  print('-----------------------------------')
  print(sns)
  print(msg)
  print('-----------------------------------')


def publish_meetup():
  meetup_client = meetup.api.Client(api_key=key_dict['meetup'])

  evt = meetup_client.CreateEvent(
      name='test title',
      duration=None,
      email_reminders=True,
      group_id=23255845,
      group_urlname='Seoul-Artificial-Intelligence',
      guest_limit=2,
      host_instructions='',
      hosts='203189175,189944980',
      how_to_find_us='',
      publish_status='published',
      question_0='',
      rsvp_alerts=True,
      rsvp_limit=80,
      rsvp_open=1531058912000,
      rsvp_close=1531663711000,
      simple_html_description='test',
      description='test',
      time=1531663711000,
      venue_id=25567071,  # hpct
      venue_visibility='public',
      waitlisting='off',
      why=''
  )
  # result
  # print(evt.__dict__)


def get_meetup_event():
  meetup_client = meetup.api.Client(api_key=key_dict['meetup'])

  evt = meetup_client.GetEvents(
      group_id=23255845,
      group_urlname='Seoul-Artificial-Intelligence',
      status="upcoming"
      # time = epoch time,
  )

  upcoming_evt = evt.results[0]

  event = dict(
      id=upcoming_evt['id'],
      name=upcoming_evt['name'],
      duration=upcoming_evt['duration'],
      created=upcoming_evt['created'],
      group_id=upcoming_evt['group']['id'],
      group_urlname=upcoming_evt['group']['urlname'],
      event_url=upcoming_evt['event_url'],
      rsvp_limit=upcoming_evt['rsvp_limit'],
      description=re.sub(
          '<[^<]+?>', '',
          upcoming_evt['description'].replace('</p>', '</p>\n').replace('<p>', '<p>\n')),
      time=upcoming_evt['time'],
      venue=upcoming_evt['venue'],
  )

  return event


def publish_twitter(evt, command, photo_dir):
  twitter_client = twitter.Api(consumer_key=key_dict['twitter']['consumer_key'],
                               consumer_secret=key_dict['twitter']['consumer_secret'],
                               access_token_key=key_dict['twitter']['access_token_key'],
                               access_token_secret=key_dict['twitter']['access_token_secret'])
  msg = '{prefix_msg} {name} {event_url}'.format(
      prefix_msg='Upcoming event of SeoulAI!',
      name=evt['name'],
      event_url=evt['event_url'])

  if command == TEST:
    print_event('twitter', msg)
  elif command == FIRE:
    twitter_client.PostUpdate(msg)
  elif command == PHOTO:
    pass


def publish_slack(evt, command, photo_dir):
  slack = Slacker(key_dict['slack'])

  msg = '{description} {event_url}'.format(
      description=evt['description'],
      event_url=evt['event_url']
  )
  if command == TEST:
    print_event('slack', msg)
  elif command == FIRE:
    slack.chat.post_message('#general', msg)
  elif command == PHOTO:
    pass


def publish_facebook(evt, command, photo_dir):
  msg = ''

  if command == TEST:
    print_event('facebook', msg)
  elif command == FIRE:
    pass
  elif command == PHOTO:
    pass


def publish_mail(evt, command, photo_dir):
  msg = ''

  if command == TEST:
    print_event('mail', msg)
  elif command == FIRE:
    pass
  elif command == PHOTO:
    pass


def parse_arguments(parser):
  parser.add_argument('command', type=str, metavar='<command>',
                      help='automation command (fire, test, photo)')
  parser.add_argument('--photo_dir', type=str, default='photo/',
                      help='The path to the directory containing photos. If you just post event, do not use this option')

  args = parser.parse_args()
  return args


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  args = parse_arguments(parser)

  evt = get_meetup_event()
  publish_twitter(evt, command=args.command, photo_dir=args.photo_dir)
  publish_slack(evt, command=args.command, photo_dir=args.photo_dir)
  publish_facebook(evt, command=args.command, photo_dir=args.photo_dir)
  publish_mail(evt, command=args.command, photo_dir=args.photo_dir)
