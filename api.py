from flask import Flask, jsonify, request

import jsonpickle
import methods
import parse

app = Flask(__name__)


@app.route('/currentMp', methods=['GET'])
def get_current_mp():
    link = request.args.get('l')
    username = request.args.get('u')
    password = request.args.get('p')
    soup = methods.main(username, password, link, -1)

    marking_periods = []
    for x in soup:
        classes = x.findAll("div", {"class": "AssignmentClass"})
        marking_periods.append(parse.main(classes))

    return jsonpickle.encode(marking_periods[0], unpicklable=False)


@app.route('/pastMp', methods=['GET'])
def get_past_mp():
    link = request.args.get('l')
    username = request.args.get('u')
    password = request.args.get('p')
    soup = methods.main(username, password, link, -2)

    marking_periods = []
    for x in soup:
        classes = x.findAll("div", {"class": "AssignmentClass"})
        marking_periods.append(parse.main(classes))

    return jsonpickle.encode(marking_periods, unpicklable=False)


@app.route('/mp', methods=['GET'])
def get_mp():
    link = request.args.get('l')
    username = request.args.get('u')
    password = request.args.get('p')
    mp = int(request.args.get('mp'))
    soup = methods.main(username, password, link, mp)

    marking_periods = []
    for x in soup:
        classes = x.findAll("div", {"class": "AssignmentClass"})
        marking_periods.append(parse.main(classes))

    return jsonpickle.encode(marking_periods[0], unpicklable=False)


@app.route('/login', methods=['GET'])
def get_valid_login():
    link = request.args.get('l')
    username = request.args.get('u')
    password = request.args.get('p')
    return methods.login(username, password, link)


if __name__ == '__main__':
    app.run()
    # debug, host='0.0.0.0', port=80
