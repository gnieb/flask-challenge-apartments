from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Apartment(db.Model, SerializerMixin):
    __tablename__ = 'apartments'

    serialize_rules= ('-leases',)

    id = db.Column(db.Integer, primary_key = True)
    number = db.Column(db.Integer, nullable = False)
    leases = db.relationship('Lease', backref='apartment')
    tenants = association_proxy('leases', 'tenant')

    @validates('number')
    def validate_num(self, key, num):
        if num < 1:
            raise ValueError("Number is invalid")
        return num

class Tenant(db.Model, SerializerMixin):
    __tablename__ = 'tenants'

    serialize_rules=('-leases.tenant', '-leases.apartment')

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    leases = db.relationship('Lease', backref='tenant')
    apartments=association_proxy('leases', 'apartment')


    @validates('age')
    def validate_num(self, key, num):
        if num < 18:
            raise ValueError("Age must be 18 or older!")
        return num    

class Lease(db.Model, SerializerMixin):
    __tablename__ = 'leases'

    serialize_rules =('-tenant.leases', '-apartment.leases')

    id = db.Column(db.Integer, primary_key = True)
    rent = db.Column(db.Integer, nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))


