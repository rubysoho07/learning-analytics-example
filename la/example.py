import json
import datetime

from pymongo import MongoClient
from bson import ObjectId
from flask import Flask, render_template, request, abort, session, redirect, url_for

from la.caliper_event import *

app = Flask(__name__)
app.secret_key = 'U9dvcDH1pvn6zSOgZZBrweHy9lvB6Shd'


# Database configuration
lrs = MongoClient('localhost')['LRS']['CaliperEvents']


def _check_login():
    if 'username' in session.keys():
        return True
    else:
        return False


@app.route('/')
def index():
    if 'username' in session.keys():
        logged_in = True
        username = session['username']
    else:
        logged_in = False
        username = None

    return render_template('index.html', logged_in=logged_in, username=username)


@app.route('/login')
def login():
    session['username'] = 'test_user'

    # Create Caliper SessionEvent (LoggedIn)
    save_session_event(True, session['username'])
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    # Create Caliper SessionEvent (LoggedOut)
    save_session_event(False, session['username'])

    session.pop('username')

    return redirect(url_for('index'))


@app.route('/reading')
def reading():

    if _check_login() is False:
        return redirect(url_for('index'))

    save_navigation_event(session['username'])

    return render_template('reading.html')


@app.route('/tag', methods=['POST'])
def tag_page():
    """
    Generate tag and send AnnotationEvent
    """
    if _check_login() is False:
        return redirect(url_for('index'))

    tags = list(tag for tag in request.form['tags'].split(','))

    save_annotation_event(session['username'], tags)

    return render_template('reading.html', tags=tags)


@app.route('/assessment')
def assessment_page():
    """ Starting assessment. """

    if _check_login() is False:
        return redirect(url_for('index'))

    save_assessment_event_started(session['username'])

    return render_template('assessment.html')


@app.route('/assessment_submit', methods=['POST'])
def assessment_submit():
    """ Submit student's answer for the assessment. """

    if _check_login() is False:
        return redirect(url_for('index'))

    answer = int(request.form['test-question'])

    if answer == 1:
        score = 10.0
    else:
        score = 0.0

    save_assessment_event_submitted_grade_event(session['username'], score)

    return render_template('assessment.html', answer=answer)


@app.route('/endpoint', methods=['POST'])
def endpoint():
    """ Endpoint to save learning record. """
    if request.method == 'POST':
        data = json.loads(request.data)

        for event in data['data']:
            result = lrs.insert(event)

            if type(result) is not ObjectId:
                abort(500)

        return "Inserting events completed!"
    else:
        abort(400)


def _get_records_by_date(date):
    """ Get learning records from LRS (Querying by specific date) """
    result = lrs.find({
        "actor.name": session['username'],
        "_id": {
            "$gt": ObjectId.from_datetime(date),
            "$lt": ObjectId.from_datetime(date + datetime.timedelta(days=1))
        }
    }, {
        "actor.name": 1,
        "action": 1,
        "eventTime": 1,
        "object.name": 1
    })

    return result


def _get_today_event_summary(today):
    """ Retrieve summarized today's events. """
    today_events = list()

    for event in _get_records_by_date(today):
        event_time = datetime.datetime.strptime(event['eventTime'], '%Y-%m-%dT%H:%M:%S.%fZ')\
            .replace(tzinfo=datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=9)))

        obj = {
            'actor': event['actor']['name'],
            'action': event['action'],
            'eventTime': event_time,
            'object': event['object']['name']
        }
        today_events.append(obj)

    return today_events


def _get_grade_comparison():
    """ Get my grade and average grade of the group I belong. """

    my_grade = lrs.find({
        "type": "GradeEvent",
        "actor.name": session['username'],
        "object.assignable.id": "http://example.org/assessment/1"
    }, {
        "generated.scoreGiven": 1
    })[0]

    average_grade = list(lrs.aggregate([
        {
            "$match": {
                "type": "GradeEvent",
                "object.assignable.id": "http://example.org/assessment/1"
            }
        },
        {
            "$group": {
                "_id": None,
                "average_score": {
                    "$avg": "$generated.scoreGiven"
                }
            }
        }
    ]))[0]

    return {
        "my_score": my_grade['generated']['scoreGiven'],
        "average_score": average_grade['average_score']
    }


@app.route('/dashboard')
def dashboard():

    if _check_login() is False:
        return redirect(url_for('index'))

    # 1일 단위 학습활동 기록
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0,
                                              tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
    today_events = _get_today_event_summary(today)

    # 동일 그룹 내 성적 비교하기
    grade_comparison = _get_grade_comparison()

    return render_template('dashboard.html', today_events=today_events, today=today, grade_comparison=grade_comparison)
