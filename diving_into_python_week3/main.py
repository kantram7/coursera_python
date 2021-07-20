from solution import *

car = Car('Bugatti Veyron', 'bugatti.png', '0.312', '2')
print(car.car_type, car.brand, car.photo_file_name, car.carrying, car.passenger_seats_count, sep='\n')

# car
# Bugatti Veyron
# bugatti.png
# 0.312
# 2

cars = get_car_list('cars.csv')
print(len(cars))  # 4

for car in cars:
    print(type(car))
