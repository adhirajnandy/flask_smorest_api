from flask  import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from schemas import StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel

blp = Blueprint("stores", __name__, description="Operations on stores")

##routes consisting store id in the url
@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id) 
        return store
    
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return{"message":"Store deleted!"}


##routes /store
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    #For creating a store
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data): 
        #inserting data into the database
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
            400,
            message="A store with that name already exists.",
        )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store
        
