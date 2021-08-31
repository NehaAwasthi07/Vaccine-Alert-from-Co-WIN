import time
from cowin_script_functions import *

no_attempts = 450

i = 0
while i < no_attempts:
    print(i)
    try:
        results = make_request()
    except:
        results = []

    available_slots = check_available(results)

    if len(available_slots) > 0:
        send_email(available_slots)
        print('slots found')
        time.sleep(60)
        # break
    else:
        time.sleep(10)

    i = i + 1


