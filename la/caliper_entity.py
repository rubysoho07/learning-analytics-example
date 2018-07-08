import datetime

from caliper import entities

__all__ = [
    'get_attempt',
    'get_group',
    'get_score',
    'get_software_application',
    'get_tags',
    'get_user',
    'get_web_page',
    'get_assessment'
]


def get_user(user):
    return entities.Person(id='http://example.org/person/' + user, name=user)


def get_software_application():
    return entities.SoftwareApplication(id='http://example.org/app/testservice', name='Learning Analytics Example')


def get_group():
    return entities.Group(id='http://example.org/group/test', name='1학년 3반')


def get_web_page():
    return entities.WebPage(id='http://example.org/textbook/1', name='불법 행위와 범죄(교과서)')


def get_tags(user, tags):
    return entities.TagAnnotation(
        id="http://example.org/textbook/1/tag/1",
        name="불법 행위와 범죄(교과서) 태그",
        annotator=get_user(user),
        annotated=get_web_page(),
        tags=tags
    )


def get_attempt(user):
    return entities.Attempt(
        id="http://example.org/assessment/1/attempt/1",
        name="불법 행위와 범죄 평가(첫 번째 시도)",
        assignee=get_user(user),
        assignable=get_assessment(),
        count=1
    )


def get_score(score):
    return entities.Score(
        id="http://example.org/assessment/1/attempt/1/score",
        attempt="http://example.org/assessment/1/attempt/1",
        name="불법 행위와 범죄 평가(첫 번째 시도)",
        maxScore=10.0,
        scoreGiven=score,
        dateCreated=datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
    )


def get_assessment():
    return entities.Assessment(id='http://example.org/assessment/1', name='불법 행위와 범죄'
                                                                          '(평가)')
