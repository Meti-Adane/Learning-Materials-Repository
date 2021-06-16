from cerberus import Validator
from flask import Response, json



def validate_arg(arg):
    try:
        arg = int(arg)
    except Exception as e:
        return Response(json.dumps({"Message":"Invalid argument passed"}), status=400)


def valdiate_book(data):
    validate_schema = {
        'title': {
            'type': 'string',
            'required': True,
            'empty': False,
            'maxlength': 500 
        },

        'author':{
            'type': 'string',
            'required': True,
            'empty': False,
            'maxlength': 100
        },
        'isbn': {
            'type': 'string',
            'required': True,
            'empty': False,
            'maxlength': 100
        },
        'publisher': {
            'type': 'string',
            'empty': False,
            'maxlength': 100
        },
        'description':{
            'type':'string'
        },
        'publish_date':{
            
        },
        'edition':{

        },
        'image_file':{

        },
        'skill_level':{

        },
        'book_file':{

        }
    }