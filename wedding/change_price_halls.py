import time
from datetime import date
from .models import Regulation, Hall, DateOfOrganization

year, month, day, hour, minute = map(int, time.strftime("%Y %m %d %H %M").split())
day = date.today()


def price_hall_now():
    try:
        regulation = Regulation.objects.last()
        halls = Hall.objects.filter(active=True)
        for hall in halls:
            weekday = 0
            if day.weekday() in (5, 6):
                weekday = regulation.weekend_price
            hall.morning_price = hall.price * float(regulation.morning_price) + weekday
            hall.noon_price = hall.price * regulation.noon_price + weekday
            hall.night_price = hall.price * regulation.night_price + weekday
            hall.save()
    except:
        pass
    # else:
    #     for hall in halls:
    #         weekday = 0
    #         if day.weekday() in (5, 6):
    #             weekday = regulation.weekend_price
    #         hall.morning_price = hall.price * float(regulation.morning_price) + weekday
    #         hall.noon_price = hall.price * regulation.noon_price + weekday
    #         hall.night_price = hall.price * regulation.night_price + weekday
    #         hall.save()


# price_hall_now(day)




