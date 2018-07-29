import datetime

import caliper
from caliper import entities, events
from caliper.constants import CALIPER_ACTIONS

from la.caliper_entity import *

__all__ = [
    'save_assessment_event_started',
    'save_annotation_event',
    'save_navigation_event',
    'save_session_event',
    'save_assessment_event_submitted_grade_event'
]

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
        actor=get_user(user),
        action=CALIPER_ACTIONS['LOGGED_IN'] if is_login is True else CALIPER_ACTIONS['LOGGED_OUT'],
        object=get_software_application(),
        eventTime=datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=get_group()
    )
    sensor.send(event)


def save_navigation_event(user):

    # Create and send NavigationEvent
    event = events.NavigationEvent(
        actor=get_user(user),
        action=CALIPER_ACTIONS['NAVIGATED_TO'],
        object=get_web_page(),
        eventTime=datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=get_group()
    )

    sensor.send(event)


def save_annotation_event(user, tags):

    # Tag
    generated_tag = entities.TagAnnotation(
        id="http://example.org/textbook/1/tag/1",
        annotator=get_user(user),
        annotated=get_web_page(),
        tags=tags
    )

    # Create and send AnnotationEvent
    event = events.AnnotationEvent(
        actor=get_user(user),
        action=CALIPER_ACTIONS['TAGGED'],
        object=get_web_page(),
        generated=generated_tag,
        eventTime=datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=get_group()
    )

    sensor.send(event)


def save_assessment_event_started(user):
    assessment_event = events.AssessmentEvent(
        actor=get_user(user),
        action=CALIPER_ACTIONS['STARTED'],
        object=get_assessment(),
        eventTime=datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=get_group()
    )

    sensor.send(assessment_event)


def save_assessment_event_submitted_grade_event(user, score):
    assessment_event = events.AssessmentEvent(
        actor=get_user(user),
        action=CALIPER_ACTIONS['SUBMITTED'],
        object=get_assessment(),
        eventTime=datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=get_group()
    )

    grade_event = events.GradeEvent(
        actor=get_user(user),
        action=CALIPER_ACTIONS['GRADED'],
        object=get_attempt(user),
        generated=get_score(score),
        eventTime=datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=get_group()
    )
    
    sensor.send([assessment_event, grade_event])
