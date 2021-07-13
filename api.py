from flask import Flask, jsonify, request

import jsonpickle
import methods
import parse

app = Flask(__name__)


class MarkingPeriod:
    def __init__(self, courses, mp):
        self.courses = courses
        self.mp = mp


class MpResponse:
    def __init__(self, mp):
        self.mp = mp


class CurrentMpResponse:
    def __init__(self, mp):
        self.currentMp = mp


class PastMpResponse:
    def __init__(self, mps):
        self.pastMps = mps


@app.route('/currentMp', methods=['GET'])
def get_current_mp():
    link = request.args.get('l')
    username = request.args.get('u')
    password = request.args.get('p')
    res = methods.main(username, password, link, -1)

    marking_periods = []
    for x in res:
        classes = x[0].findAll("div", {"class": "AssignmentClass"})
        marking_periods.append(MarkingPeriod(parse.main(classes), x[1]))

    return jsonpickle.encode(CurrentMpResponse(marking_periods[0]), unpicklable=False)


@app.route('/pastMp', methods=['GET'])
def get_past_mp():
    link = request.args.get('l')
    username = request.args.get('u')
    password = request.args.get('p')
    res = methods.main(username, password, link, -2)

    marking_periods = []
    for x in res:
        classes = x[0].findAll("div", {"class": "AssignmentClass"})
        marking_periods.append(MarkingPeriod(parse.main(classes), x[1]))

    return jsonpickle.encode(PastMpResponse(marking_periods), unpicklable=False)


@app.route('/mp', methods=['GET'])
def get_mp():
    link = request.args.get('l')
    username = request.args.get('u')
    password = request.args.get('p')
    mp = int(request.args.get('mp'))
    res = methods.main(username, password, link, mp)

    marking_periods = []
    for x in res:
        classes = x[0].findAll("div", {"class": "AssignmentClass"})
        marking_periods.append(MarkingPeriod(parse.main(classes), x[1]))

    return jsonpickle.encode(MpResponse(marking_periods[0]), unpicklable=False)


@app.route('/login', methods=['GET'])
def get_valid_login():
    link = request.args.get('l')
    username = request.args.get('u')
    password = request.args.get('p')
    return jsonpickle.encode(methods.login(username, password, link), unpicklable=False)


if __name__ == '__main__':
    app.run()
    # debug, host='0.0.0.0', port=80
