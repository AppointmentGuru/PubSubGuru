from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.enums import PNStatusCategory

import importlib, os

class PubNubBackend:
    '''
    Usage:

    **Subscribe**
    ```
    pubsub = PubNubBackend(channel, pub_key, sub_key)
    pubsub.subscribe()
    ```

    Requires environment variables:
    * PUBNUB_PUBLISH_KEY
    * PUBNUB_SUBSCRIBE_KEY

    '''

    def __init__(self, channel):

        publish_key = os.environ.get('PUBNUB_PUBLISH_KEY', None)
        subscribe_key = os.environ.get('PUBNUB_SUBSCRIBE_KEY', None)

        if None in [subscribe_key, publish_key]:
            msg = 'Please make sure you\'ve set environment varialbes: PUBNUB_PUBLISH_KEY and PUBNUB_SUBSCRIBE_KEY'
            raise Exception(msg)

        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = subscribe_key
        pnconfig.publish_key = publish_key
        pnconfig.ssl = False
        self.channel = channel
        self.pubnub = PubNub(pnconfig)

    def publish(self, key, payload):
        def publish_callback(result, status):

            if result:
                print(result)
            if status.error is not None:
                raise Exception('PubSub publish error: {}: {}'\
                    .format(status.error, status.error_data))
        data = {
            "key": key,
            "payload": payload
        }
        self.pubnub.publish()\
            .channel(self.channel)\
            .message(data)\
            .async(publish_callback)

    def subscribe(self, functionmapper):
        '''
        Implements a multicast pub/sub. It is the responsibility of the
        subscriber determine if it needs to perform any actions based on
        the message key

        functionmapper is a dict that maps payload keys to methods to call
        Methods will receive the payload as the first argument.

        e.g.:

        ```
        functionmapper = {
            'test': {
                'module': 'config',
                'method': 'foo'
            }
        }
        ```
        '''
        my_listener = SubscribeListener()
        self.pubnub.add_listener(my_listener)

        self.pubnub.subscribe().channels(self.channel).execute()
        # self.pubnub.add_channel_to_channel_group()\
        #     .channel_group("test")\
        #     .channels(channels)\
        #     .sync()

        my_listener.wait_for_connect()
        print('connected')

        while True:
            result = my_listener.wait_for_message_on(self.channel)
            print(result.message)
            task_definition = functionmapper.get(result.message.get('key'), None)
            if task_definition is not None:
                mod = importlib.import_module(task_definition.get('module'))
                method = task_definition.get('method')
                getattr(mod, method)(result.message)

