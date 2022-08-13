import json
from time import sleep
from flask import Flask, request
import threading

app = Flask(__name__)

tokenQueue = []
threadList = []
clinicLimit = {
    '1': 3,
    '2': 5
}

def taskRunner(clinicId, userId):
    clinicBookedToken = [i for i in tokenQueue if i['clinicId'] == clinicId]
    if len(clinicBookedToken):
        sleep(15)
        # remove booked token
        tokenQueue[:] = [d for d in tokenQueue if d.get('clinicId') != clinicId and  d.get('userId') != userId]

        # recursive
        taskRunner(clinicId, userId)
    else:
        # thread close
        threadList.remove(threading.current_thread().name)

@app.route("/")
def home():
    reqData = request.get_json()
    clinicId = reqData['clinicId']
    userId = reqData['userId']

    print(len(threading.enumerate()))

    # add in queue
    tokenQueue.append({'clinicId': clinicId, 'userId': userId})

    # start new thread
    if not 'clinic-'+str(clinicId) in threadList:
        threadList.append('clinic-'+str(clinicId))
        threading.Thread(target=taskRunner, args=(clinicId, userId), name='clinic-'+str(clinicId)).start()

    # send response
    response = app.response_class(
        response=json.dumps(tokenQueue),
        status=200,
        mimetype='application/json'
    )

    return response


# isClinicExist =  next((item for item in tokenQueue if item['clinicId'] == clinicId), None)
# if isClinicExist :
#     print(isClinicExist)
#     isClinicExist['tokenCount'] += 1
# else:
#     tokenQueue.append({'clinicId': clinicId, 'tokenCount': 0})


# previous booked token
# clinicBookedToken = [i for i in tokenQueue if i['clinicId'] == clinicId]

# # limit exceeded
# if not clinicLimit[str(clinicId)] > len(clinicBookedToken):
#     return app.response_class(
#         response=json.dumps({'message': 'Token limit execeeded'}),
#         status=200,
#         mimetype='application/json'
#     )
