# Testing

## Enable test mode

Either set `SWAMPDRAGON_TESTMODE = True` in settings, or set environment var `SWAMPDRAGON_TESTMODE = True`.

Enabling test mode will set the test publisher and test subscriber, and data will be added to in-memory dictionaries rather than written to Redis.


## DragonTestCase

Use `DragonTestCase` when creating test cases for routers.

*  `last_message`: The last message sent to the connection
*  `last_pub`: The last published message received by the connection
*  `subscribe`: Subscribe to a channel
*  `unsubscribe`: Unsubscribe from a channel
*  `call_verb`: Call the router


## Example test case
 
    from swampdragon.tests.dragon_test_case import DragonTestCase
    
    
    class FooTest(DragonTestCase):
        def test_foo(self):
            self.connection.call_verb('foo-route', 'do_foo', bar='test')
            message = self.connection.last_message
            self.assertEqual(message['data']['bar'], 'test')
