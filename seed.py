from faker import Faker
from random import randint
from app.database import SessionLocal
from app import models
from app.models import ShipmentStatus, UserRole
from app.schemas import UserRole
from sqlalchemy import select, func


faker = Faker()

def seed():
    db = SessionLocal()
    try:
        # 1. Create clients
        for i in range(0):
            new_country_code = faker.country_code()
            new_client_id = new_country_code + "-" + str(randint(1, 100))
            new_name = faker.company()
            new_email = faker.email()
            new_address = faker.address()
            new_telephone = faker.phone_number()

            db_client = models.Client(
                client_id=new_client_id,
                name= new_name,
                address = new_address,
                email = new_email,
                telephone = new_telephone
            )
            db.add(db_client)

        # 2. Create users
        for i in range(0):
            db_user_client = models.User(
                username = faker.user_name(),
                hashed_password = "admin12345",
                role = UserRole.client_user
            )
            db.add(db_user_client)

        for i in range(0):
            db_employee = models.User(
                username = faker.user_name(),
                hashed_password = "admin12345",
                role = UserRole.employee
            )
            db.add(db_employee)


        # 3. Assign Users to Clients
        for i in range (0):
            #find random id in all users
            all_users = select(func.count("*")).select_from(models.User)
            random_user = randint(1, db.execute(all_users).scalars().first())

            #find random client
            all_clients = select(func.count("*")).select_from(models.Client)
            random_client = randint(1, db.execute(all_clients).scalars().first())

            db_connection = models.UserClient(
                user_id = random_user,
                client_id = random_client
            )
            db.add(db_connection)


        # 4. create shipments
        for i in range (10):
            all_clients = select(func.count("*")).select_from(models.Client)
            random_id = randint(1, db.execute(all_clients).scalars().first())
            search_client = select(models.Client).where(models.Client.id == random_id)
            result = db.execute(search_client).scalars().one()

            shipment_client = result.client_id
            origin_code = faker.country_code()
            dest_code = faker.country_code()
            shipment_tracking = origin_code + "-" + dest_code + "-" + str(randint(1,999))

            statuses = list(ShipmentStatus)
            random_status = randint(0,3)

            db_shipment = models.Shipment(
                status = statuses[random_status],
                client_id = shipment_client,
                tracking_number = shipment_tracking,
                origin = origin_code,
                destination = dest_code
            )
            db.add(db_shipment)

            


        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
