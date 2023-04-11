from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Apartment, Tenant, Lease

app = Flask( __name__ )
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///apartments.db'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )
db.init_app( app )

api = Api(app)

class Home(Resource):
    def get(self):
        return make_response({"Hey there!": "You're doing grrrrrrrreat!"}, 200)

api.add_resource(Home, '/')

class Apartments(Resource):
    def get(self):
        apartments = [a.to_dict() for a in Apartment.query.all()]

        return make_response(
            apartments,
            200
        )
    
    def post(self):
        data = request.get_json()

        try:
            new_apartment = Apartment(
            number=data['number']
            )
            db.session.add(new_apartment)
            db.session.commit()
        except:
            db.session.rollback()
            return make_response({"error": "Unable to create new apartment"})
        
        return make_response(new_apartment.to_dict(), 201)
    
    
api.add_resource(Apartments, '/apartments')

class ApartmentById(Resource):
    def get(self, id):
        apartment = Apartment.query.filter_by(id=id).first().to_dict()
        return make_response(apartment, 200)
    
    def patch(self, id):
        apartment = Apartment.query.filter_by(id=id).first()
        if not apartment:
            return make_response({"message":"apartment not found"})
        
        data = request.get_json()
        for key in data.keys():
            setattr(apartment, key, data[key])
        
        db.session.add(apartment)
        db.session.commit()

        return make_response(apartment.to_dict(), 202)
    
    def delete(self, id):
        apartment = Apartment.query.filter_by(id=id).first()
        if not apartment:
            return make_response({"message":"apartment not found"})
        
        db.session.delete(apartment)
        db.session.commit()

        return make_response({"message": "apartment deleted"}, 202)

api.add_resource(ApartmentById, '/apartments/<int:id>')

class Tenants(Resource):
    def get(self):
        tenants = [t.to_dict() for t in Tenant.query.all()]

        return make_response(tenants, 200)

    def post(self):

        data = request.get_json()
        try:
            new_tenant = Tenant(name=data['name'], age=data['age'])
            db.session.add(new_tenant)
            db.session.commit()
        except:
            return make_response({"error":"unable to create new tenant!"}, 404)
        
        return make_response(new_tenant.to_dict(), 201)

api.add_resource(Tenants, '/tenants')

class TenantById(Resource):
    def get(self, id):
        tenant = Tenant.query.filter_by(id=id).first().to_dict()
        if not tenant:
            return make_response({"message": "tenant not found!"}, 404)
        
        return make_response(tenant, 200)
    
    def patch(self, id):
        tenant = Tenant.query.filter_by(id=id).first()
        if not tenant:
            return make_response({"message": "tenant not found!"}, 404)
        
        try:
            data = request.get_json()
            for key in data.keys():
                setattr(tenant, key, data[key])
            db.session.add(tenant)
            db.session.commit()
        except:
            return make_response({"error":"unable to update tenant"}, 404)

        return make_response(tenant.to_dict(), 201)
    
    def delete(self, id):
        tenant = Tenant.query.filter_by(id=id).first()
        if not tenant:
            return make_response({"message": "tenant not found!"}, 404)
        try:
            db.session.delete(tenant)
            db.session.commit()
        except:
            return make_response({"error":"unable to delete tenant"})
        return make_response({"message": "tenant deleted!!!"})
    
api.add_resource(TenantById, '/tenants/<int:id>' )
    
class Leases(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_lease= Lease(
                rent=data['rent'], 
                apartment_id=data['apartment_id'], 
                tenant_id=data['tenant_id'] 
                )
            db.session.add(new_lease)
            db.session.commit()
        except:
            return make_response({"error":"unable to create new lease"}, 404)
        return make_response(new_lease.to_dict(), 201)


api.add_resource(Leases, '/leases')

class LeaseById(Resource):
    def delete(self, id):
        lease = Lease.query.filter_by(id=id).first()
        if not lease:
            return make_response({"error":"lease not found!"}, 404)
        
        try:
            db.session.delete(lease)
            db.session.commit()
        except:
            return make_response({"error": "unable to delete!"})

        return make_response({"message":"lease deleted"})
    
api.add_resource(LeaseById,'/leases/<int:id>')

if __name__ == '__main__':
    app.run( port = 3000, debug = True )