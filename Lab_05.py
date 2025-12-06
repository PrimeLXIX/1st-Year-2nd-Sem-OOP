class AppointmentScheduler:
    def __init__(self):
        self.appointment_list = []
        self.member_list = []

    def add_member(self, member):
        self.member_list.append(member)

    def add_attendance(self, topic, member):
        for appointment in self.appointment_list:
            if appointment.topic == topic:
                appointment.add_attn(member)

    def add_appointment(self, appointment):
        self.appointment_list.append(appointment)

    def edit_appointment(self, title=None, location=None, date=None, to=None):
        for appointment in self.appointment_list:
            if title and appointment.topic == title:
                appointment.topic = to
            elif location and appointment.location == location:
                appointment.location = to
            elif date and appointment.date == date:
                appointment.date = to

    def delete_appointment(self, title=None, location=None, date=None):
        self.appointment_list = [
            appointment for appointment in self.appointment_list
            if not ((title and appointment.topic == title) or
                    (location and appointment.location == location) or
                    (date and appointment.date == date))
        ]

    def view_appointments(self):
        for appointment in self.appointment_list:
            print(appointment.record())

    def show_person_in_appointment(self, member):
        for appointment in self.appointment_list:
            if appointment.attn:
                for attendance in appointment.attn:
                    if attendance.name == member.name:
                        print(appointment.record())

    def send_notifications(self, topic, message):
        for appointment in self.appointment_list:
            if appointment.topic == topic:
                if appointment.type == "Activity":
                    for member in self.member_list:
                        member.notification(message)
                else:
                    for attendance in appointment.attn:
                        attendance.notification(message)


class Appointment:
    def __init__(self, topic, location, date, attn=None, type=None):
        self.topic = topic
        self.location = location
        self.date = date
        self.attn = attn if attn else []
        self.type = type

    def __str__(self):
        pass

    def add_attn(self, member):
        if member not in self.attn:
            self.attn.append(member)

    def attendance(self):
        return ", ".join([attendance.name for attendance in self.attn]) if self.attn else "None"

    def record(self):
        record = f"{ f"{self.type}," if self.type else ''}Topic: {self.topic}, Location: {self.location}, on {self.date} "
        if self.type != "Activity":
            record += f"Attn: {self.attendance()}"
        return record.strip()

    def edit_appointment(self, title=None, location=None, date=None, to=None):
        if title and self.topic == title:
            self.topic = to
        if location and self.location == location:
            self.location = to
        if date and self.date == date:
            self.date = to


class One_time_appointment(Appointment):
    type = "One-time AP"

    def __str__(self):
        return f"Topic: {self.topic}, Location: {self.location}, on {self.date}, Attn: {self.attendance()}"


class Weekly_appointment(Appointment):
    type = "Weekly AP"

    def __init__(self, topic, location, day_of_week, attn=None):
        super().__init__(topic, location, day_of_week, attn, type="Weekly AP")

    def __str__(self):
        return f"Weekly AP, Topic: {self.topic}, Location: {self.location}, on {self.date}, Attn: {self.attendance()}"


class Activity(Appointment):
    type = "Activity"

    def __init__(self, topic, location, date):
        super().__init__(topic, location, date, type="Activity")

    def __str__(self):
        return f"Activity, Topic: {self.topic}, Location: {self.location}, on {self.date}"


class Member:
    def __init__(self, name, email, telephone_number, noti_type):
        self.name = name
        self.email = email
        self.telephone_number = telephone_number
        self.noti_type = noti_type
        self.noti = email if noti_type == "email" else telephone_number

    def notification(self, message):
        print(f"Sending {self.noti_type} notification to: {self.noti} with message: {message}")


# Testing
app = AppointmentScheduler()

# Add Members
john = Member("John Doe", "john.doe@example.com", None, "email")
jane = Member("Jane Smith", "jane.smith@example.com", None, "email")
robert = Member("Robert Johnson", "robert.johnson@example.com", "08-1234-5678", "SMS")
emily = Member("Emily Davis", "emily.davis@example.com", "08-3456-7890", "SMS")

app.add_member(john)
app.add_member(jane)
app.add_member(robert)
app.add_member(emily)


# # Test Case 1 : Add Appointment, add activity information, and add appointment information.
# 1 : title="Team Meeting #1", location="Room A" , date="2024-03-15", Jane Smith, Robert Johnson,  Emily Davis
# 2 : title="Team Meeting #2", location="Room B" , date="2024-03-17", Jane Smith, Robert Johnson และ Emily Davis
# 3 : title="Weekly Meeting", location="Room C" , day_of_week="Wednesday"
# Activity
# 4 : title="Company Party", location="Conference Room", date="2024-03-17"
# 5 : title="Company Visit", location="Conference Room", date="2024-03-17"

# Output Expect
# Topic : Team Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis
# Topic : Team Meeting #2 Location : Room B on 2024-03-17 Attn: Jane Smith,John Doe,Emily Davis
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17

print()
print("Test Case 1 : Add Appointment, add activity information, and add appointment information.")
print()
app.add_appointment(One_time_appointment("Team Meeting #1", "Room A", "2024-03-15", [jane, robert, emily]))
app.add_appointment(One_time_appointment("Team Meeting #2", "Room B", "2024-03-17", [jane, robert, emily]))
app.add_appointment(Weekly_appointment("Weekly Meeting", "Room C", "Wednesday", [john, robert, emily]))
app.add_appointment(Activity("Company Party", "Conference Room", "2024-03-17"))
app.add_appointment(Activity("Company Visit", "Conference Room", "2024-03-17"))
app.view_appointments()            # Show all Appointments
print("----------------------------------------------------------------------------------------------------------")
print()

# # Test Case 2 : Edit Appointment 
# Change the name of One-Time Appointment #1 from “Team Meeting #1” to “Team B Meeting #1”
# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis
# Topic : Team Meeting #2 Location : Room C on 2024-03-17 Attn: Jane Smith,John Doe,Emily Davis
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17
print("Test Case 2 : Edit Appointment")
print()
app.edit_appointment(title = "Team Meeting #1", to = "Team B Meeting #1")
app.edit_appointment(location = "Room B", to = "Room C")
app.view_appointments()            # Show all Appointments
print("----------------------------------------------------------------------------------------------------------")
print()


# # Test Case 3 : Delete Appointment using topic “Team Meeting #2” 
# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17
print("Test Case 3 : Delete Appointment using topic “Team Meeting #2”")
print()
app.delete_appointment(title = "Team Meeting #2")
app.view_appointments()            # Show all Appointments
print("----------------------------------------------------------------------------------------------------------")
print()

# # Test Case 4 : Add Attendance who receives appointments for one-time appointments and weekly appointments as follows.
# - One-Time Appointment #1 (“Team B Meeting #1”) Add John Doe
# - Weekly Appointments “Weekly Meeting” added Jane Smith.

# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis,John Doe
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis,Jane Smith
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17
print("Test Case 4 : Add Attendance who receives appointments for one-time appointments and weekly appointments")
print()
app.add_attendance("Team B Meeting #1", john)
app.add_attendance("Weekly Meeting", jane)
app.view_appointments()            # Show all Appointments
print("----------------------------------------------------------------------------------------------------------")
print()

# # Test Case 5 : Search Attendance Search for individual appointments using the name “Robert Johnson”. 
# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis,John Doe
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis,Jane Smith
print("Test Case 5 : Search Attendance Search for individual appointments using the name Robert Johnson")
print()
app.show_person_in_appointment(john)
print("----------------------------------------------------------------------------------------------------------")
print()

# # Test Case 6 : Notify by using the appointment “Team B Meeting #1”
# Output Expect
# Sending email notification to: jane.smith@example.com with message : invite for meeting
# Sending SMS notification to: 08-1234-5678 with message : invite for meeting
# Sending SMS notification to: 08-3456-7890 with message : invite for meeting
# Sending email notification to: john.doe@example.com with message : invite for meeting
print("Test Case 6 : Notify by using the appointment “Team B Meeting #1")
print()
app.send_notifications("Team B Meeting #1","invite for meeting")
print("----------------------------------------------------------------------------------------------------------")
print()