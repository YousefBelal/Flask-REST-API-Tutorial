from datetime import date
from flask import Flask,request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import func
from datetime import date

app = Flask(__name__)
api = Api(app)
app.config['DATABASE_URL'] = 'postgres://feyqwkonocxeos:7af21936784101aa5e0cd7030b3e777d6c2e506d65e7867fbe71da185e7fd7f7@ec2-54-173-237-110.compute-1.amazonaws.com:5432/d28fqlnbl8s1gh'
db = SQLAlchemy(app)

class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)
	date=db.Column(db.Date, nullable=False)

	def __repr__(self):
		return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes},date = {self.date})"



video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)
video_put_args.add_argument("date", type=date, help="date of the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}

class Video(Resource):
	@marshal_with(resource_fields)
	def get(self, video_id):
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="Could not find video with that id")
		return result

	@marshal_with(resource_fields)
	def put(self, video_id):
		args = video_put_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		if result:
			abort(409, message="Video id taken...")

		video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'],date=args['date'])
		db.session.add(video)
		db.session.commit()
		return video, 201

	@marshal_with(resource_fields)
	def patch(self, video_id):
		args = video_update_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="Video doesn't exist, cannot update")

		if args['name']:
			result.name = args['name']
		if args['views']:
			result.views = args['views']
		if args['likes']:
			result.likes = args['likes']

		db.session.commit()

		return result

	@marshal_with(resource_fields)
	def delete(self, video_id):
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="Video doesn't exist, cannot delete")
		db.session.delete(result)
		db.session.commit()
		return {"message":"This video has been deleted successfully"} ,204




@app.route('/api/test_date', methods=['POST'])
def add_entry():
	args=request.get_json()
	video = VideoModel(name=args['name'], views=args['views'], likes=args['likes'],date=args['date'])
	db.session.add(video)
	db.session.commit()

	return	"entry added!!!!"

@app.route('/api/get_date', methods=['GET'])
def get_date():
	list1=[]
	d="2022-09-03"
	format = "%Y-%m-%d"
	dt_object = datetime.datetime.strptime(d, format)
	videos = db.session.query(VideoModel).filter(func.date(VideoModel.date) > dt_object.date()).all()
	for video in videos:
		data={
			"date":video.date
		}
		list1.append(data)


	return	{"m":list1}

if __name__ == "__main__":
	api.add_resource(Video, "/video/<int:video_id>")
	app.run()