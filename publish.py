# -*- coding: utf-8 -*-
import yaml
import meetup.api


with open("config.yml", 'r') as ymlfile:
  cfg = yaml.load(ymlfile)
key_dict = cfg['apikey']


def publish_meetup():
  client = meetup.api.Client()
  client.api_key = key_dict['meetup']
  evt = client.CreateEvent(
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
  print(evt.__dict__)


if __name__ == "__main__":
  publish_meetup()
