import os
import json

from datetime import datetime

from caliper import entities, events
from caliper.constants import CALIPER_ACTIONS

import requests

from la.caliper_entity import *

__all__ = [
    'save_assessment_event_started',
    'save_annotation_event',
    'save_navigation_event',
    'save_session_event',
    'save_assessment_event_submitted_grade_event'
]

SENSOR_HOST = os.environ['SENSOR_HOST']


def _send_event(event: dict):
    event_str = json.dumps(event, ensure_ascii=False)

    requests.post(SENSOR_HOST,
                  data=event_str.encode(),
                  headers={"Content-Type": "application/json"})


def save_session_event(is_login, user):
    event = events.SessionEvent(
        actor=get_user(user),
        action=CALIPER_ACTIONS['LOGGED_IN'] if is_login is True else CALIPER_ACTIONS['LOGGED_OUT'],
        object=get_software_application(),
        eventTime=datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=get_group()
    )

    _send_event(event.as_dict(thin_props=True, thin_context=True))


def save_navigation_event(user):

    # Create and send NavigationEvent
    event = events.NavigationEvent(
        actor=get_user(user),
        action=CALIPER_ACTIONS['NAVIGATED_TO'],
        object=get_web_page(),
        eventTime=datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=get_group()
    )

    _send_event(event.as_dict(thin_props=True, thin_context=True))


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
        eventTime=datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=get_group()
    )

    _send_event(event.as_dict(thin_props=True, thin_context=True))


def save_assessment_event_started(user):
    assessment_event = events.AssessmentEvent(
        actor=get_user(user),
        action=CALIPER_ACTIONS['STARTED'],
        object=get_assessment(),
        eventTime=datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=get_group()
    )

    _send_event(assessment_event.as_dict(thin_props=True, thin_context=True))


def save_assessment_event_submitted_grade_event(user, score):
    assessment_event = events.AssessmentEvent(
        actor=get_user(user),
        action=CALIPER_ACTIONS['SUBMITTED'],
        object=get_assessment(),
        eventTime=datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=get_group()
    )

    grade_event = events.GradeEvent(
        actor=get_user(user),
        action=CALIPER_ACTIONS['GRADED'],
        object=get_attempt(user),
        generated=get_score(score),
        eventTime=datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        group=get_group()
    )

    _send_event(assessment_event.as_dict(thin_props=True, thin_context=True))
    _send_event(grade_event.as_dict(thin_props=True, thin_context=True))
