# import math
# import random
# import datetime
# import os

# now = datetime.datetime.now()
# # Math module
# print(math.factorial(5))

# # Random module
# print(random.randint(1, 10))

# # Datetime module
# print("Current date and time: " + now.strftime(" Date: %Y-%m-%d Time: %H:%M:%S"))

# # OS module
# print(os.getcwd())

import datetime
import time

while True:
    now = datetime.datetime.now()
    print(now.strftime("Current date and time: %Y-%m-%d %H:%M:%S"), end="\r")
    time.sleep(1)