from flask import Flask, jsonify, request

import jsonpickle
import methods
import parse

app = Flask(__name__)


@app.route('/grades', methods=['GET'])
def get_grades():
    link = request.args.get('l')
    username = request.args.get('u')
    password = request.args.get('p')
    soup = methods.main(username, password, link)
    classes = soup.findAll("div", {"class": "AssignmentClass"})

    main_grade = parse.main(classes)

    return jsonpickle.encode(main_grade, unpicklable=False)


if __name__ == '__main__':
    app.run()
    # debug, host='0.0.0.0', port=80
