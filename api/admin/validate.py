from cerberus import Validator
from flask import Response, json



def validate_arg(arg):
    try:
        arg = int(arg)
    except Exception as e:
        return Response(json.dumps({"Message":"Invalid argument passed"}), status=400)