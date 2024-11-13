from flask_project import db, bcrypt, app
from flask_project.models import Admin, Customer, Service, Service_Request, Service_Professional

with app.app_context():
    db.create_all()

def db_setup_rbac():
    with app.app_context():
        admin_list = Admin.query.all()
        if not admin_list:
            
            hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
            admin_user = Admin(id=-1, username='admin', email='admin@test.com', password=hashed_password) 
            db.session.add(admin_user)
            db.session.commit()

    with app.app_context():
        
        customer_list = Customer.query.all()
        if not customer_list:
            dummy_customer = Customer(
                id=1001, 
                username='dummy_customer', 
                password='dummy_password', 
                address="123 Dummy Street, Nowhere", 
                email='dummy_customer@gmail.com', 
                contact='1234565432' 
            )
            db.session.add(dummy_customer)
            db.session.commit()

        
        service_list = Service.query.all()
        if not service_list:
            
            services = [
                Service(name='Cleaning', price='50', description='cleaning service'), 
                 Service(name='Washing', price='50', description='washing service'), 
            ]
            db.session.bulk_save_objects(services) 
            db.session.commit()

        
        service_professional_list = Service_Professional.query.all()
        if not service_professional_list:
            
            service_ids = [Service.query.first_or_404().id]

            
            x = 0
            for service_id in service_ids:
                dummy_service_professional = Service_Professional(
                    id=10001, 
                    username=f'dummy_professional_{x}', 
                    password='dummy_password', 
                    email=f'dummy_professional_{x}@gmail.com', 
                    description='Experienced household service provider', 
                    experience="5 years", 
                    service_id=service_id 
                )
                x += 1
                db.session.add(dummy_service_professional)
            db.session.commit()

if __name__ == "__main__":
    db_setup_rbac()
    app.run(host='0.0.0.0', debug=True, port=5001)
