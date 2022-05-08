from flask import Flask, request
from respect_validation import FormValidator as fv, Validator as v

app = Flask(__name__)


@app.route("/")
def hello_world():
    if request.method == 'GET':
        return "It works!"
    else:
        user = request.json
        validator = fv()
        validator.validate(user, {
            "username": v.stringType().alnum().noWhitespace().length(4, 32).Not(
                v.oneOf(v.equals('admin'), v.equals('root'))),
            "email": v.Optional(v.email()),
            "first_name": v.Optional(v.length(3, 32).alpha(' ')),
            "second_name": v.Optional(v.length(3, 32).alpha(' ')),
            "personal_id": v.IntVal().positive().Min(1),
            "password": v.length(8, 64).Not(
                v.anyOf(v.lowercase(), v.uppercase(), v.IntVal(), v.alpha(),
                        v.phone(), v.email())).alnum(' ', '!\'"#$%&''()*+,‐./:;<=>?@')
        })
        if validator.failed():
            return {"validation": validator.get_messages()}, 200

        return {"validation": None}, 200
