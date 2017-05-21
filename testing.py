from datetime import datetime, timedelta

first = datetime.now()

second = first + timedelta(seconds=10)

while second > datetime.now():
    print(datetime.now())
