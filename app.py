from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import MetaData

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres@db/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

db.Model.metadata = MetaData(naming_convention=dict(
    ix='ix_%(column_0_label)s',
    uq="uq_%(table_name)s_%(column_0_name)s",
    ck="ck_%(table_name)s_%(constraint_name)s",
    fk="fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    pk="pk_%(table_name)s"
))


class AuditMixin:
    @declared_attr
    def created_by_id(cls):
        return db.Column(db.Integer,
                         db.ForeignKey('user.id', name='fk_%s_created_by_id' % cls.__tablename__,
                                       use_alter=True))

    @declared_attr
    def created_by(cls):
        return db.relationship(
            'User',
            primaryjoin='User.id == %s.created_by_id' % cls.__name__,
            remote_side='User.id'
        )

    @declared_attr
    def updated_by_id(cls):
        return db.Column(db.Integer,
                         db.ForeignKey('user.id', name='fk_%s_updated_by_id' % cls.__tablename__,
                                       use_alter=True))

    @declared_attr
    def updated_by(cls):
        return db.relationship(
            'User',
            primaryjoin='User.id == %s.updated_by_id' % cls.__name__,
            remote_side='User.id'
        )


class User(db.Model, AuditMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=True)
    password = db.Column(db.String(200), nullable=False)


@app.route("/")
def index():
    return "Hello"


if __name__ == '__main__':
    db.create_all()
    app.run()
