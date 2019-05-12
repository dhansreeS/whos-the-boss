from app import db
from datetime import datetime


class UserLines(db.Model):
    """
    Create a data model for the database to be set up for capturing user inputs to view trends in how the app is being used

    """
    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.String(300), unique=False, nullable=False)
    time = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<UserLines %r>' % self.user_input
