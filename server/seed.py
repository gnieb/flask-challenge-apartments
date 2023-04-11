
from app import app
from models import db, Tenant, Lease, Apartment



if __name__ == '__main__':
        with app.app_context():
                
                Apartment.query.delete()
                Tenant.query.delete()
                Lease.query.delete()
                
                t1 = Tenant(name='grace', age=27)
                t2 = Tenant(name='noah', age=25)
                t3 = Tenant(name='sam', age=40)


                a1 = Apartment(number=1)
                a2 = Apartment(number=2)
                a3 = Apartment(number=3)


                l1 = Lease(rent=400, tenant_id=1, apartment_id=1)
                l2 = Lease(rent=500, tenant_id=1, apartment_id=2)
                l3 = Lease(rent=800, tenant_id=1, apartment_id=3)

                db.session.add_all([t1, t2, t3, a1, a2, a3, l1, l2, l3])
                db.session.commit()

