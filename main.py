from abc import ABC, abstractmethod
import json
import os
import logging

# JSON faylga ma'lumot saqlash
def save_data(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

# JSON fayldan ma'lumotni yuklash
def load_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return json.load(file)
    return []

# Logger sozlamalari
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(message)s")
def log_action(action):
    logging.info(action)

# Person bazaviy klassi
class Person(ABC):
    def __init__(self, first_name, last_name, age, username):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.username = username

    @abstractmethod
    def get_role(self):
        pass

# Passenger va Driver classlari
class Passenger(Person):
    def get_role(self):
        return "Yo‘lovchi"

class Driver(Person):
    def __init__(self, first_name, last_name, age, username, license_number):
        super().__init__(first_name, last_name, age, username)
        self.license_number = license_number

    def get_role(self):
        return "Haydovchi"

# Transport bazaviy klassi
class Transport(ABC):
    def __init__(self, name, number, color, driver: Driver):
        self.name = name
        self.number = number
        self.color = color
        self.driver = driver

    @abstractmethod
    def move(self):
        pass

# Transport turlari
class Bus(Transport):
    def move(self):
        return f"{self.name} ({self.number}) avtobusi belgilangan yo‘nalish bo‘ylab harakatlanmoqda."

class Metro(Transport):
    def move(self):
        return f"{self.name} ({self.number}) metrosi yer ostida harakatlanmoqda."

# Address va Route classlari
class Address:
    def __init__(self, location):
        self.location = location

class Route:
    def __init__(self, start: Address, end: Address, stops: list):
        self.start = start
        self.end = end
        self.stops = stops

    def get_route_info(self):
        return f"Yo‘nalish: {self.start.location} → {', '.join([stop.location for stop in self.stops])} → {self.end.location}"

# Ticket classi
class Ticket:
    def __init__(self, transport: Transport, price: float, passenger: Passenger):
        self.transport = transport
        self.price = price
        self.passenger = passenger

    def get_ticket_info(self):
        return f"{self.passenger.first_name} {self.passenger.last_name} uchun chipta: {self.transport.name} ({self.transport.number}), Narxi: {self.price} so‘m"

# Username unikal ekanligini tekshirish
def is_username_unique(username):
    users = load_data("users.json")
    return not any(user["username"] == username for user in users)

# Raqamli kiritishni tekshirish
def get_integer_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Iltimos, raqam kiriting!")

# Ro‘yxatdan o‘tish funksiyasi
def register_user():
    print("\n--- R o‘yxatdan o‘tish ---")
    print("1. Yo‘lovchi")
    print("2. Haydovchi")
    while True:
        tanlov = input("Tanlovni kiriting (1 yoki 2): ")
        if tanlov == "1":
            first_name = input("Ismingizni kiriting: ")
            last_name = input("Familiyangizni kiriting: ")
            age = get_integer_input("Yoshingizni kiriting: ")
            while True:
                username = input("Foydalanuvchi nomini kiriting: ")
                if is_username_unique(username):
                    break
                print("Bu foydalanuvchi nomi allaqachon mavjud. Boshqa nom tanlang.")
            user = Passenger(first_name, last_name, age, username)
            role = "passenger"
            break
        elif tanlov == "2":
            first_name = input("Ismingizni kiriting: ")
            last_name = input("Familiyangizni kiriting: ")
            age = get_integer_input("Yoshingizni kiriting: ")
            while True:
                username = input("Foydalanuvchi nomini kiriting: ")
                if is_username_unique(username):
                    break
                print("Bu foydalanuvchi nomi allaqachon mavjud. Boshqa nom tanlang.")
            license_number = input("Haydovchilik guvohnomasi raqamini kiriting: ")
            user = Driver(first_name, last_name, age, username, license_number)
            role = "driver"
            break
        else:
            print("Noto‘g‘ri tanlov! Qaytadan urinib ko‘ring.")

    # Ma'lumotlarni saqlash
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
    log_action(f"{user.first_name} {user.last_name} ro'yxatdan o'tdi.")
    print(f"\n{user.first_name} {user.last_name}, siz {user.get_role()} sifatida ro‘yxatdan o‘tdingiz!")
    return user

# Foydalanuvchini yuklash
def load_user(username):
    users = load_data("users.json")
    for user_data in users:
        if user_data["username"] == username:
            if user_data["role"] == "passenger":
                return Passenger(user_data["first_name"], user_data["last_name"], user_data["age"], user_data["username"])
            elif user_data["role"] == "driver":
                return Driver(user_data["first_name"], user_data["last_name"], user_data["age"], user_data["username"], user_data["license_number"])
    return None

# Chipta narxini hisoblash
def calculate_ticket_price(route):
    base_price = 10000
    stop_multiplier = 5000
    return base_price + (len(route.stops) * stop_multiplier)

# Asosiy menyu
def main():
    print("\n=== Jamoat transporti boshqaruv tizimi ===")
    username = input("Foydalanuvchi nomingizni kiriting: ")
    user = load_user(username)
    if not user:
        print("Siz ro'yxatdan o'tmagansiz. Iltimos, ro'yxatdan o'ting.")
        user = register_user()
    log_action(f"{user.first_name} {user.last_name} tizimga kirish qildi.")
    print(f"\nXush kelibsiz, {user.first_name} {user.last_name}!")

    # Transport obyektlarini yaratish
    driver1 = Driver("Ali", "Karimov", 35, "alikarimov", "DL12345")
    bus1 = Bus("Shahar Avtobusi", "B123", "Ko‘k", driver1)
    metro1 = Metro("Toshkent Metropoliteni", "M10", "Qizil", driver1)

    # Yo‘nalishlar
    address_start = Address("Toshkent")
    address_end = Address("Samarqand")
    stops = [Address("Jizzax"), Address("Guliston")]
    route1 = Route(address_start, address_end, stops)

    # Chipta yaratish
    ticket_price = calculate_ticket_price(route1)
    ticket1 = Ticket(bus1, ticket_price, user)

    while True:
        print("\n=== Menyu ===")
        print("1. Transport harakatini ko‘rish (Avtobus yoki metro harakati haqida ma'lumot)")
        print("2. Yo‘nalish haqida ma’lumot olish (Yo'nalish va bekatlar ro'yxati)")
        print("3. Chipta xarid qilish (Tanlangan transport uchun chipta xaridi)")
        print("4. Dasturdan chiqish")
        tanlov = input("Tanlovni kiriting: ")

        if tanlov == "1":
            print(bus1.move())
        elif tanlov == "2":
            print(route1.get_route_info())
        elif tanlov == "3":
            print(ticket1.get_ticket_info())
        elif tanlov == "4":
            print("Dastur tugatildi.")
            log_action(f"{user.first_name} {user.last_name} tizimdan chiqdi.")
            break
        else:
            print("Noto‘g‘ri tanlov! Qaytadan urinib ko‘ring.")

# Dastur ishga tushirilishi
if __name__ == "__main__":
    main()