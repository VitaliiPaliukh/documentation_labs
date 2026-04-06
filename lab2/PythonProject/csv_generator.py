"""CSV Generator Module - Creates dental clinic data CSV file with 1000+ records"""
import csv
import random
from datetime import datetime, timedelta


class DentalDataGenerator:
    """Generates dental clinic data for CSV file"""

    def __init__(self):
        self.patient_names = [
            "Іванов Іван", "Петренко Петро", "Сидоренко Олена", "Коваленко Марія",
            "Бондаренко Олександр", "Ткаченко Наталія", "Шевченко Андрій", "Кравченко Юлія",
            "Мельник Сергій", "Морозова Катерина", "Зайцев Михайло", "Соколова Ірина",
            "Павленко Дмитро", "Литвиненко Анна", "Гончаренко Василь", "Романенко Світлана",
            "Семененко Віктор", "Кузьменко Оксана", "Денисенко Богдан", "Поліщук Тетяна",
            "Левченко Артем", "Ковальчук Людмила", "Волков Роман", "Савченко Валентина",
            "Новак Максим", "Білоус Галина", "Руденко Ігор", "Гриценко Євгенія",
            "Федоренко Вадим", "Данилова Софія", "Назаренко Павло", "Терещенко Дарина",
            "Лисенко Олег", "Марченко Алла", "Кравчук Володимир", "Панченко Ольга"
        ]

        self.doctor_names = [
            "Доктор Смірнов Олексій", "Доктор Козлова Тетяна", "Доктор Васильєв Ігор",
            "Доктор Михайлова Вікторія", "Доктор Новіков Сергій", "Доктор Федорова Олена",
            "Доктор Морозов Андрій", "Доктор Волкова Наталія", "Доктор Соловйов Петро",
            "Доктор Лебедєва Марина"
        ]

        self.specializations = [
            "Ортодонт", "Хірург", "Терапевт", "Ортопед", "Пародонтолог"
        ]

        self.diagnoses = [
            "Карієс", "Пульпіт", "Періодонтит", "Гінгівіт", "Пародонтит",
            "Стоматит", "Зубний камінь", "Ерозія емалі", "Клиноподібний дефект",
            "Флюороз", "Альвеоліт", "Абсцес", "Неправильний прикус"
        ]

        self.service_names_xray = [
            "Панорамний знімок", "Прицільний знімок", "КТ щелепи",
            "Цифрова рентгенографія", "3D томографія"
        ]

        self.service_names_surgery = [
            "Видалення зуба", "Імплантація", "Резекція верхівки кореня",
            "Пластика ясен", "Кістна пластика", "Синус-ліфтинг"
        ]

        self.image_resolutions = ["1024x768", "1920x1080", "2560x1440", "3840x2160"]
        self.anesthesia_types = ["Місцева", "Загальна", "Седація", "Провідникова"]

    def generate_phone(self):
        """Generate random Ukrainian phone number"""
        return f"+380{random.randint(50, 99)}{random.randint(1000000, 9999999)}"

    def generate_insurance(self):
        """Generate random insurance number"""
        return f"INS{random.randint(100000, 999999)}"

    def generate_license(self):
        """Generate random doctor license"""
        return f"LIC{random.randint(10000, 99999)}"

    def generate_date(self):
        """Generate random appointment date in the last year"""
        start_date = datetime.now() - timedelta(days=365)
        random_days = random.randint(0, 365)
        random_hours = random.randint(8, 18)
        random_minutes = random.choice([0, 15, 30, 45])
        date = start_date + timedelta(days=random_days)
        return date.replace(hour=random_hours, minute=random_minutes, second=0, microsecond=0)

    def generate_csv(self, filename: str, num_records: int = 1000):
        """Generate CSV file with dental clinic data"""
        print(f"Generating {num_records} records...")

        # Create unique patients and doctors
        patients = {}
        doctors = {}

        for i in range(min(100, num_records // 10)):
            insurance = self.generate_insurance()
            patients[insurance] = {
                'name': random.choice(self.patient_names),
                'phone': self.generate_phone(),
                'insurance': insurance
            }

        for i in range(len(self.doctor_names)):
            license = self.generate_license()
            doctors[license] = {
                'name': self.doctor_names[i],
                'phone': self.generate_phone(),
                'license': license,
                'specialization': random.choice(self.specializations)
            }

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'patient_name', 'patient_phone', 'patient_insurance',
                'doctor_name', 'doctor_phone', 'doctor_license', 'doctor_specialization',
                'appointment_date', 'appointment_status',
                'diagnosis', 'total_cost',
                'service_name', 'service_price', 'service_type', 'service_attr1', 'service_attr2'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for i in range(num_records):
                patient = random.choice(list(patients.values()))
                doctor = random.choice(list(doctors.values()))

                # Randomly choose service type
                if random.random() < 0.5:
                    service_type = 'xray'
                    service_name = random.choice(self.service_names_xray)
                    service_attr1 = random.choice(self.image_resolutions)
                    service_attr2 = str(round(random.uniform(0.1, 2.0), 2))
                    service_price = round(random.uniform(200, 1000), 2)
                else:
                    service_type = 'surgery'
                    service_name = random.choice(self.service_names_surgery)
                    service_attr1 = random.choice(self.anesthesia_types)
                    service_attr2 = str(random.randint(1, 5))
                    service_price = round(random.uniform(1000, 10000), 2)

                row = {
                    'patient_name': patient['name'],
                    'patient_phone': patient['phone'],
                    'patient_insurance': patient['insurance'],
                    'doctor_name': doctor['name'],
                    'doctor_phone': doctor['phone'],
                    'doctor_license': doctor['license'],
                    'doctor_specialization': doctor['specialization'],
                    'appointment_date': self.generate_date().strftime('%Y-%m-%d %H:%M:%S'),
                    'appointment_status': random.choice(['SCHEDULED', 'COMPLETED', 'CANCELED']),
                    'diagnosis': random.choice(self.diagnoses),
                    'total_cost': service_price,
                    'service_name': service_name,
                    'service_price': service_price,
                    'service_type': service_type,
                    'service_attr1': service_attr1,
                    'service_attr2': service_attr2
                }
                writer.writerow(row)

                if (i + 1) % 100 == 0:
                    print(f"Generated {i + 1} records...")

        print(f"Successfully generated {num_records} records in {filename}")


def main():
    """Main function to run CSV generator"""
    import sys

    num_records = 1000
    if len(sys.argv) > 1:
        try:
            num_records = int(sys.argv[1])
        except ValueError:
            print("Invalid number of records. Using default: 1000")

    generator = DentalDataGenerator()
    generator.generate_csv('dental_data.csv', num_records)


if __name__ == '__main__':
    main()
