import datetime

import caliper
from caliper import entities, events
from caliper.constants import CALIPER_ACTIONS

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
        actor=entities.Person(id='http://example.org/person/' + user, name=user),
        action=CALIPER_ACTIONS['LOGGED_IN'] if is_login is True else CALIPER_ACTIONS['LOGGED_OUT'],
        object=entities.SoftwareApplication(id='http://example.org/app/testservice', name='Learning Analytics Example'),
        eventTime=datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=entities.Group(id='http://example.org/group/test', name='testgroup')
    )
    sensor.send(event)


def save_navigation_event(user):

    # Create and send AnnotationEvent
    event = events.NavigationEvent(
        actor=entities.Person(id='http://example.org/person/' + user, name=user),
        action=CALIPER_ACTIONS['NAVIGATED_TO'],
        object=entities.WebPage(id='http://example.org/textbook/1', name='Textbook'),
        eventTime=datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=entities.Group(id='http://example.org/group/test', name='testgroup')
    )

    sensor.send(event)


def save_annotation_event(user, tags):

    # Tag
    generated_tag = entities.TagAnnotation(
        id="http://example.org/textbook/1/tag/1",
        annotator=entities.Person(id='http://example.org/person/' + user, name=user),
        annotated=entities.WebPage(id='http://example.org/textbook/1', name='Textbook'),
        tags=tags
    )

    # Create and send AnnotationEvent
    event = events.AnnotationEvent(
        actor=entities.Person(id='http://example.org/person/' + user, name=user),
        action=CALIPER_ACTIONS['TAGGED'],
        object=entities.WebPage(id='http://example.org/textbook/1', name='Textbook'),
        generated=generated_tag,
        eventTime=datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=entities.Group(id='http://example.org/group/test', name='testgroup')
    )

    sensor.send(event)


def save_assessment_event_started(user):
    assessment_event = events.AssessmentEvent(
        actor=entities.Person(id='http://example.org/person/' + user, name=user),
        action=CALIPER_ACTIONS['STARTED'],
        object=entities.Assessment(id='http://example.org/assessment/1', name='불법 행위와 범죄 평가'),
        eventTime=datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=entities.Group(id='http://example.org/group/test', name='testgroup')
    )

    sensor.send(assessment_event)


def save_assessment_event_submitted_grade_event(user, score):
    assessment_event = events.AssessmentEvent(
        actor=entities.Person(id='http://example.org/person/' + user, name=user),
        action=CALIPER_ACTIONS['SUBMITTED'],
        object=entities.Assessment(id='http://example.org/assessment/1', name='불법 행위와 범죄 평가'),
        eventTime=datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=entities.Group(id='http://example.org/group/test', name='testgroup')
    )

    attempt = entities.Attempt(
        id="http://example.org/assessment/1/attempt/1",
        assignee=entities.Person(id='http://example.org/person/' + user, name=user),
        assignable=entities.Assessment(id='http://example.org/assessment/1', name='불법 행위와 범죄 평가'),
        count=1
    )

    score = entities.Score(
        id="http://example.org/assessment/1/attempt/1",
        attempt=attempt,
        maxScore=10.0,
        scoreGiven=score,
        dateCreated=datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
    )

    grade_event = events.GradeEvent(
        actor=entities.Person(id='http://example.org/person/' + user, name=user),
        action=CALIPER_ACTIONS['GRADED'],
        object=attempt,
        generated=score,
        eventTime=datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=entities.Group(id='http://example.org/group/test', name='testgroup')
    )
    
    sensor.send([assessment_event, grade_event])
