#!/usr/bin/python

import sys, time, random
from pubsub import get_backend, publish, listen
from faker import Faker
fake = Faker()

FUNCTION_MAPPER = {
    'foo': {
        'module': 'example',
        'method': 'foo'
    }
}

def foo(data):
    res = json.loads(json.dumps(m.get('data').decode('utf-8')))
    print("<< Message received: {}".format(res))


# def message_received():
#     print "<< message received: "

BACKEND = 'RedisBackend' # options: RedisBackend, PubNubBackend, ..

def publisher():
    '''
    Publishes a random blob of data after a random number of seconds
    '''
    backend = get_backend('backends', BACKEND, 'my.app')
    for x in range(0,100):
        data = fake.pydict()

        print("-----------------------")
        publish(backend, 'foo', data)
        sleeptime = random.choice(range(1,10))
        time.sleep(sleeptime)

def subscribe():
    '''
    listen for things getting published
    '''
    backend = get_backend('backends', BACKEND, 'my.app')
    listen(backend, FUNCTION_MAPPER)

if __name__ == "__main__":
    print(str(sys.argv))
    if (len(sys.argv) == 1):
        publisher()
    else:
        subscribe()