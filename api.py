from flask import Flask, jsonify

import methods
import parse

app = Flask(__name__)


@app.route('/grades/<username>/<password>/<link>', methods=['GET'])
def get_grades(username, password, link):
    soup = methods.main(username, password, link)
    classes = soup.findAll("div", {"class": "AssignmentClass"})

    main_grade = parse.main(classes)

    return jsonify(main_grade)


if __name__ == '__main__':
    app.run(debug=True)
    #, host='0.0.0.0', port=80
