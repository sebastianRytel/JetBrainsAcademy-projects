# from flask import Flask
# from flask_restful import Api, Resource
# import sys
# from flask_restful import inputs
# from flask_restful import reqparse
#
# app = Flask(__name__)
#
# # write your code here
#
# api = Api(app)
#
# class HelloWorldResource(Resource):
#     def get(self):
#         return {"data":"There are no events for today!"}
#
#
# api.add_resource(HelloWorldResource, '/event/today')
#
# # do not change the way you run the program
# if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         arg_host, arg_port = sys.argv[1].split(':')
#         app.run(host=arg_host, port=arg_port)
#     else:
#         app.run()

###############################################################################
###############################################################################
###############################################################################

# from flask import Flask
# from flask_restful import Api, Resource
# from flask_restful import inputs
# from flask_restful import reqparse
# import sys
#
# app = Flask(__name__)
# api = Api(app)
#
# parser = reqparse.RequestParser()
#
# parser.add_argument(
#     'event',
#     type=str,
#     help="The event name is required!",
#     required=True
# )
#
# parser.add_argument(
#     'date',
#     type=inputs.date,
#     help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
#     required=True
# )
#
# events_json = {}
#
# class HelloWorldResource(Resource):
#     def get(self):
#         return {"data":"There are no events for today!"}
#     def post(self):
#         args = parser.parse_args()
#         events_json['message'] = "The event has been added!"
#         events_json['event'] = args['event']
#         events_json['date'] = str(args['date'].date())
#         return events_json
#
# api.add_resource(HelloWorldResource, '/event')
#
# # # do not change the way you run the program
# if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         arg_host, arg_port = sys.argv[1].split(':')
#         app.run(host=arg_host, port=arg_port)
#     else:
#         app.run()

###############################################################################
###############################################################################
###############################################################################

from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_restful import Api, Resource, marshal_with, fields, marshal
from flask_restful import inputs, reqparse, request
import sys


app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
parser = reqparse.RequestParser()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///name.db'

class Event(db.Model):
    __tablename__ = 'table_name'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
db.create_all()

parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)

parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)

event_serializer = {
    "id":fields.Integer,
    'event':fields.String,
    'date':fields.DateTime(dt_format='iso8601')
}

def dateToobject(date):
    list_ = [int(number) for number in date.split('-')]
    return datetime.date(list_[0], list_[1], list_[2])

class Event_API_current(Resource):
    @marshal_with(event_serializer)
    def get(self):
        return Event.query.filter(Event.date == datetime.date.today()).all()

class Event_API(Resource):
    @marshal_with(event_serializer)
    def get(self):
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        if start_time:
            list_event_dates = []
            x = dateToobject(start_time)
            y = dateToobject(end_time)
            for el in Event.query.all():
                if x <= el.date <= y:
                    list_event_dates.append(el)
            return list_event_dates
        else:
            return Event.query.all()

    def post(self):
        args = parser.parse_args()
        event = Event(event=args['event'], date=args['date'])
        db.session.add(event)
        db.session.commit()
        return {'message' : "The event has been added!",
                'event' : args['event'],
                'date' : str(args['date'].date())
        }

class EventByID(Resource):
    @marshal_with(event_serializer)
    def get(self, id):
        event = Event.query.filter(Event.id == id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        return event

class EventDelete(Resource):
    def delete(self, id):
        event = Event.query.filter(Event.id == id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        db.session.delete(event)
        db.session.commit()
        return {"message": "The event has been deleted!"
                }

api.add_resource(EventDelete, '/event/<int:id>')
api.add_resource(EventByID, '/event/<int:id>')
api.add_resource(Event_API_current, '/event/today')
api.add_resource(Event_API, '/event')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
