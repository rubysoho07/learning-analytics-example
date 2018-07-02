import datetime

import caliper
from caliper import entities, events
from caliper.constants import CALIPER_ACTIONS

# Caliper configuration
sensor_config = caliper.HttpOptions(
    host='http://localhost:5000/endpoint',
    auth_scheme='Bearer',
    api_key='Test'
)

sensor = caliper.build_sensor_from_config(
    sensor_id='https://example.org/sensor',
    config_options=sensor_config
)


def save_session_event(is_login, user):
    event = events.SessionEvent(
        actor=entities.Person(id='http://example.org/person' + user, name=user),
        action=CALIPER_ACTIONS['LOGGED_IN'] if is_login is True else CALIPER_ACTIONS['LOGGED_OUT'],
        object=entities.SoftwareApplication(id='http://example.org/app/testservice', name='Learning Analytics Example'),
        eventTime=datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=entities.Group(id='http://example.org/group/test', name='testgroup')
    )
    sensor.send(event)
