#!/usr/bin/python

import ConfigParser

config = ConfigParser.RawConfigParser()
config.add_section('settings')
config.set('settings', 'pin', '17, 4, 11, 18')
config.set('settings', 'email_enabled', 'TRUE')
config.set('settings', 'email', 'q9k6m64wyj@pomail.net')

conf = open('settings.conf', 'w')
config.write(conf)
conf.close()

