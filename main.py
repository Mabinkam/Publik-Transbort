from abc import ABC, abstractmethod
import json
import os


def save_data(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)


def load_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


class Person(ABC):
    def __init__(self, first_name, last_name, age, username):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.username = username

    @abstractmethod
    def get_role(self):
        pass


class Passenger(Person):
    def get_role(self):
        return "Yo‘lovchi"


class Driver(Person):
    def __init__(self, first_name, last_name, age, username, license_number):
        super().__init__(first_name, last_name, age, username)
        self.license_number = license_number

    def get_role(self):
        return "Haydovchi"


class Transport(ABC):
    def __init__(self, name, number, color, driver: Driver):
        self.name = name
        self.number = number
        self.color = color
        self.driver = driver

    @abstractmethod
    def move(self):
        pass


class Car(Transport):
    def move(self):
        return f"{self.name} ({self.number}) avtomobili shahar ko'chalari bo'yicha harakatlanmoqda."


class Bus(Transport):
    def move(self):
        return f"{self.name} ({self.number}) avtobusi yo'lovchilarni yetkazib bermoqda."


class Metro(Transport):
    def move(self):
        return f"{self.name} ({self.number}) metrosi yer ostida tezlik bilan harakatlanmoqda."


class Airplane(Transport):
    def move(self):
        return f"{self.name} ({self.number}) samolyoti havo orqali uzun masofalarga boradi."


class Tram(Transport):
    def move(self):
        return f"{self.name} ({self.number}) tramvayi temir yo'llar bo'yicha sekin harakatlanmoqda."


class Address:
    def __init__(self, location):
        self.location = location


class Route:
    def __init__(self, start: Address, end: Address, stops: list):
        self.start = start
        self.end = end
        self.stops = stops

    def get_route_info(self):
        return f"Yo'nalish: {self.start.location} → {', '.join([stop.location for stop in self.stops])} → {self.end.location}"


class Ticket:
    def __init__(self, transport: Transport, price: float, passenger: Passenger, route: Route):
        self.transport = transport
        self.price = price
        self.passenger = passenger
        self.route = route

    def get_ticket_info(self):
        return (
            f"{self.passenger.first_name} {self.passenger.last_name} uchun chipta:\n"
            f"Transport: {self.transport.name} ({self.transport.number})\n"
            f"Narxi: {self.price} so'm\n"
            f"Yo'nalish: {self.route.get_route_info()}"
        )


class Schedule:
    def __init__(self):
        self.schedule = {}

    def add_transport(self, transport: Transport, departure_time, arrival_time):
        self.schedule[transport.name] = {
            "departure_time": departure_time,
            "arrival_time": arrival_time
        }

    def get_schedule(self):
        schedule_info = "Transport jadvali:\n"
        for transport, times in self.schedule.items():
            schedule_info += f"{transport}: Chiqish vaqti - {times['departure_time']}, Kelish vaqti - {times['arrival_time']}\n"
        return schedule_info


def register_user():
    print("\n--- Ro'yxatdan o'tish ---")
    print("1. Yo'lovchi")
    print("2. Haydovchi")
    while True:
        tanlov = input("Tanlovni kiriting (1 yoki 2): ")
        if tanlov == "1":
            first_name = input("Ismingizni kiriting: ")
            last_name = input("Familiyangizni kiriting: ")
            age = int(input("Yoshingizni kiriting: "))
            username = input("Foydalanuvchi nomini kiriting: ")
            user = Passenger(first_name, last_name, age, username)
            role = "passenger"
            break
        elif tanlov == "2":
            first_name = input("Ismingizni kiriting: ")
            last_name = input("Familiyangizni kiriting: ")
            age = int(input("Yoshingizni kiriting: "))
            username = input("Foydalanuvchi nomini kiriting: ")
            license_number = input("Haydovchilik guvohnomasi raqamini kiriting: ")
            user = Driver(first_name, last_name, age, username, license_number)
            role = "driver"
            break
        else:
            print("Noto'g'ri tanlov! Qayta urinib ko'ring.")

    users = load_data("users.json")
    users.append({
        "role": role,
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "username": username,
        "license_number": license_number if role == "driver" else None
    })
    save_data("users.json", users)
    print(f"\n{user.first_name} {user.last_name}, siz {user.get_role()} sifatida ro'yxatdan o'tdingiz!")
    return user


def choose_transport():
    print("\n=== Transport turini tanlang ===")
    print("1. Avtobus")
    print("2. Metro")
    print("3. Mashina")
    print("4. Samolyot")
    print("5. Tramvay")

    while True:
        choice = input("Tanlovni kiriting (1-5): ")
        if choice in ["1", "2", "3", "4", "5"]:
            return choice
        else:
            print("Noto'g'ri tanlov! Qayta urinib ko'ring.")


def show_transport_info(choice, schedule):
    transports = {
        "1": {"name": "Avtobus", "info": bus1.move()},
        "2": {"name": "Metro", "info": metro1.move()},
        "3": {"name": "Mashina", "info": car1.move()},
        "4": {"name": "Samolyot", "info": airplane1.move()},
        "5": {"name": "Tramvay", "info": tram1.move()}
    }

    selected_transport = transports.get(choice)
    if selected_transport:
        print(f"\nTanlangan transport: {selected_transport['name']}")
        print(selected_transport["info"])

        # Jadvalni ham ko'rsatamiz
        print("\nTransport jadvali:")
        print(schedule.get_schedule())
    else:
        print("Noto'g'ri tanlov!")


def main():
    print("\n=== Jamoat transporti boshqaruv tizimi ===")
    username = input("Foydalanuvchi nomingizni kiriting: ")

    # Foydalanuvchini yuklash
    users = load_data("users.json")
    user = None
    for u in users:
        if u.get("username") == username:  # KeyError oldini olish uchun .get() ishlatiladi
            if u["role"] == "passenger":
                user = Passenger(u["first_name"], u["last_name"], u["age"], u["username"])
            elif u["role"] == "driver":
                user = Driver(u["first_name"], u["last_name"], u["age"], u["username"], u["license_number"])
            break

    if not user:
        print("Siz ro'yxatdan o'tmagansiz. Iltimos, ro'yxatdan o'ting.")
        user = register_user()

    print(f"\nXush kelibsiz, {user.first_name} {user.last_name}!")
    print(f"Siz {user.get_role()} sifatida ro'yxatdan o'tgansiz.")

    # Transport turini tanlash
    transport_choice = choose_transport()

    # Tanlangan transportga tegishli ma'lumotlarni ko'rsatish
    show_transport_info(transport_choice, schedule)

    # Menyu
    while True:
        print("\n=== Menyu ===")
        print("1. Transport harakati haqida ma'lumot")
        print("2. Yo'nalish haqida ma'lumot")
        print("3. Jadvalni ko'rish")
        print("4. Dasturdan chiqish")
        tanlov = input("Tanlovni kiriting: ")
        if tanlov == "1":
            show_transport_info(transport_choice, schedule)
        elif tanlov == "2":
            print(route1.get_route_info())
        elif tanlov == "3":
            print(schedule.get_schedule())
        elif tanlov == "4":
            print("Dastur tugatildi.")
            break
        else:
            print("Noto'g'ri tanlov! Qaytadan urinib ko'ring.")


# Transport obyektlarini yaratish
driver1 = Driver("Ali", "Karimov", 35, "alikarimov", "DL12345")
driver2 = Driver("Dazai", "Osuma", 22, "Dazai", "YM57535")
driver3 = Driver("William", "Moriarty", 27, "William", "WYM2722")
bus1 = Bus("Shahar Avtobusi", "B123", "Ko‘k", driver1)
metro1 = Metro("Toshkent Metropoliteni", "M10", "Qizil", driver1)
car1 = Car("Cherry", 567, "Qora", driver2)
airplane1 = Airplane("Gulfstream", 700, "Qora", driver3)
tram1 = Tram("Shahar Tramvayi", "T456", "Yashil", driver1)

# Yo'nalish
start = Address("A station")
end = Address("B station")
stops = [Address("Stop 1"), Address("Stop 2")]
route1 = Route(start, end, stops)

# Jadval
schedule = Schedule()
schedule.add_transport(bus1, "08:00", "10:00")
schedule.add_transport(metro1, "09:00", "11:00")
schedule.add_transport(car1, "09:00", "11:00")
schedule.add_transport(airplane1, "07:00", "19:00")
schedule.add_transport(tram1, "10:00", "12:00")

if __name__ == "__main__":
    main()