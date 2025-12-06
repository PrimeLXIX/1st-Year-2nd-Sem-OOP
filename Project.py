from datetime import datetime

# Base User Class
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Pet Class
class Pet:
    def __init__(self, pet_id, pet_type, owner, special_condition = ""):
        self.pet_id = pet_id
        self.pet_type = pet_type
        self.owner = owner
        self.special_condition = special_condition

# Customer Class
class Customer(User):
    def __init__(self, username, password, membership = "Basic"):
        super().__init__(username, password)
        self.membership = membership
        self.appointments = []
        self.pets = []
    
    def add_pet(self, pet):
        self.pets.append(pet)
        print(f"{self.username} added a new pet: {pet.pet_id}")
    
    def book_service(self, pet, service_code, system):
        if service_code not in system.services:
            print("Invalid service selection.")
            return
        
        price = system.services[service_code]
        appointment = {
            "pet": pet,
            "service": service_code,
            "price": price,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        self.appointments.append(appointment)
        system.appointment_history.append(appointment)
        print(f"{self.username} booked {service_code} for {pet.pet_id}. Total: ${price}")

# Staff Class
class Staff(User):
    def update_appointment(self, system, customer, pet, new_date):
        for appointment in customer.appointments:
            if appointment['pet'] == pet:
                appointment['date'] = new_date
                print(f"Appointment for {pet.pet_id} updated to {new_date}.")
                return
        print("Appointment not found.")

# Admin Class
class Admin(Staff):
    def generate_report(self, system, start_date, end_date):
        total_appointments = 0
        total_income = 0
        staff_services = {}
        
        for appointment in system.appointment_history:
            date_obj = datetime.strptime(appointment['date'], '%Y-%m-%d %H:%M')
            if start_date <= date_obj <= end_date:
                total_appointments += 1
                total_income += appointment['price']
                staff_services[appointment['service']] = staff_services.get(appointment['service'], 0) + 1
        
        print(f"Total Appointments: {total_appointments}")
        print(f"Total Income: ${total_income}")
        print("Services Provided:")
        for service, count in staff_services.items():
            print(f"{service}: {count}")
    
    def remove_customer(self, system, username):
        for customer in system.users:
            if customer.username == username:
                system.users.remove(customer)
                print(f"Removed customer: {username}")
                return
        print("Customer not found.")
    
    def remove_staff(self, system, username):
        for staff in system.staffs:
            if staff.username == username:
                system.staffs.remove(staff)
                print(f"Removed staff: {username}")
                return
        print("Staff not found.")

# Owner Class
class Owner(User):
    def modify_membership_plans(self, system, tier, discount):
        system.membership_plans[tier] = discount
        print(f"Updated {tier} membership discount to {discount * 100}%")
    
    def manage_services(self, system, service_code, new_price):
        system.services[service_code] = new_price
        print(f"Updated {service_code} service pricing to ${new_price}.")
    
    def promote_to_admin(self, system, username):
        for staff in system.staffs:
            if staff.username == username:
                new_admin = Admin(staff.username, staff.password)
                system.admins.append(new_admin)
                system.staffs.remove(staff)
                print(f"Promoted {username} to admin.")
                return
        print("User not found or not a staff member.")
    
    def remove_user(self, system, username):
        for user_list in [system.users, system.staffs, system.admins]:
            for user in user_list:
                if user.username == username:
                    user_list.remove(user)
                    print(f"Removed user: {username}")
                    return
        print("User not found.")

# Pet Spa Management System Class
class PetSpaSystem:
    def __init__(self):
        self.users = []
        self.staffs = []
        self.admins = []
        self.owners = []
        self.appointment_history = []
        self.membership_plans = {"Basic": 0, "Premium": 0.1, "VIP": 0.2}
        self.services = {
            "1a. Shampooing": 100, "1b. Trimming Dog Fur": 200,
            "2a. Cutting Nails": 65, "2b. Trimming Cat Fur": 85,
            "3a. Bird Baths": 100
        }

    def login(self, username, password):
        for user in self.users + self.staffs + self.admins + self.owners:
            if user.username == username and user.password == password:
                print(f"{username} logged in successfully.")
                return user
        print("Login failed.")
        return None
    
    def logout(self, user):
        print(f"{user.username} logged out.")
    
    def register_customer(self, username, password):
        customer = Customer(username, password)
        self.users.append(customer)
        print(f"Registered new customer: {username}")
    
    def register_staff(self, username, password):
        staff = Staff(username, password)
        self.staffs.append(staff)
        print(f"Registered new staff: {username}")
    
    def view_users(self):
        for user in self.users:
            print(f"User: {user.username}")

# Test Cases
spa_system = PetSpaSystem()
spa_system.register_customer("alice123", "pass123")
spa_system.register_customer("bob456", "pass456")
spa_system.register_customer("carol789", "pass789")
spa_system.register_customer("dave321", "pass321")

spa_system.register_staff("staff1", "staffpass1")
spa_system.register_staff("staff2", "staffpass2")

admin = Admin("admin1", "adminpass")
spa_system.admins.append(admin)

owner = Owner("owner1", "ownerpass")
spa_system.owners.append(owner)
print("---------------------------------------------------\n")

# Adding pets and booking services
alice = spa_system.users[0]
alice.add_pet(Pet(101, "Dog", "alice123"))
alice.book_service(alice.pets[0], "1a. Shampooing", spa_system)

# Adding more customers and their pets
bob = spa_system.users[1]
bob.add_pet(Pet(102, "Cat", "bob456"))
bob.book_service(bob.pets[0], "2b. Trimming Cat Fur", spa_system)

carol = spa_system.users[2]
carol.add_pet(Pet(103, "Bird", "carol789"))
carol.book_service(carol.pets[0], "3a. Bird Baths", spa_system)

dave = spa_system.users[3]
dave.add_pet(Pet(104, "Dog", "dave321"))
dave.book_service(dave.pets[0], "1b. Trimming Dog Fur", spa_system)

# Adding a new customer and their pet
spa_system.register_customer("eve654", "pass654")
eve = spa_system.users[4]
eve.add_pet(Pet(105, "Cat", "eve654"))
eve.book_service(eve.pets[0], "2a. Cutting Nails", spa_system)

# Adding another new customer and their pet
spa_system.register_customer("frank987", "pass987")
frank = spa_system.users[5]
frank.add_pet(Pet(106, "Dog", "frank987"))
frank.book_service(frank.pets[0], "1a. Shampooing", spa_system)
print("---------------------------------------------------\n")

# Viewing users before changes
spa_system.view_users()
print("---------------------------------------------------\n")

# Removing customer
admin.remove_customer(spa_system, "bob456")
spa_system.view_users()
print("---------------------------------------------------\n")

# Generating report
admin.generate_report(spa_system, datetime(2025, 1, 1), datetime(2025, 12, 31))
print("---------------------------------------------------\n")