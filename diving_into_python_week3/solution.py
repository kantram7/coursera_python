import os.path
import csv
from abc import abstractmethod


class CarBase:
    # индексы csv колонок хар-к машин
    csv_car_type = 0
    csv_brand = 1
    csv_passenger_seats_count = 2
    csv_photo_file_name = 3
    csv_body_whl = 4
    csv_carrying = 5
    csv_extra = 6

    def __init__(self, brand, photo_file_name, carrying):
        self.carrying = float(self.validate_input(carrying))
        self.brand = self.validate_input(brand)
        self.photo_file_name = self.validate_photo_filename(photo_file_name)

        if self.get_photo_file_ext() not in ['.jpg', '.jpeg', '.png', '.gif']:
            raise ValueError("Invalid img")

    @staticmethod
    def validate_input(value):
        """метод валидации данных, возвращает значение, если оно валидно,
        иначе выбрасывает исключение ValueError"""
        if value == '':
            raise ValueError
        return value

    @staticmethod
    def validate_photo_filename(filename):
        for ext in ('.jpg', '.jpeg', '.png', '.gif'):
            if filename.endswith(ext) and len(filename) > len(ext):
                return filename
        raise ValueError

    # получить расширение файла изображения
    def get_photo_file_ext(self):
        root, ext = os.path.splitext(self.photo_file_name)
        return ext

    # считать данные из строки csv
    # или лучше тут реализовать, передавая последний индекс в каждом конкретном классе ?
    @classmethod
    @abstractmethod
    def get_from_csv_row(cls, row):
        pass


class Car(CarBase):
    car_type = "car"

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(self.validate_input(passenger_seats_count))

    @classmethod
    def get_from_csv_row(cls, row):
        return cls(row[cls.csv_brand], row[cls.csv_photo_file_name], row[cls.csv_carrying],
                   row[cls.csv_passenger_seats_count])


class Truck(CarBase):
    car_type = "truck"

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)

        # параметр body_whl вида '3.92x2.09x1.87'
        try:
            length, width, height = (float(i) for i in body_whl.split('x', 2))
        except ValueError:
            length, width, height = .0, .0, .0

        self.body_length, self.body_width, self.body_height = length, width, height

    # объем кузова
    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height

    @classmethod
    def get_from_csv_row(cls, row):
        return cls(row[cls.csv_brand], row[cls.csv_photo_file_name], row[cls.csv_carrying], row[cls.csv_body_whl])


class SpecMachine(CarBase):
    car_type = "spec_machine"

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = self.validate_input(extra)

    @classmethod
    def get_from_csv_row(cls, row):
        return cls(row[cls.csv_brand], row[cls.csv_photo_file_name], row[cls.csv_carrying], row[cls.csv_extra])


def get_car_list(csv_filename):

    car_list = []  # итоговый список считаных объектов

    def cars_types(c_type, cur_row):
        return {
            Truck.car_type: Truck,
            SpecMachine.car_type: SpecMachine,
            Car.car_type: Car
        }[c_type].get_from_csv_row(cur_row)

    with open(csv_filename) as csv_table:
        reader = csv.reader(csv_table, delimiter=';')
        next(reader)  # пропускаем заголовок

        for row in reader:
            try:
                car_type = row[CarBase.csv_car_type]
                car_list.append(cars_types(car_type, row))

            except (IndexError, KeyError, ValueError):
                continue

    return car_list


if __name__ == '__main__':
    pass
