A client library for accessing live data through the SparkWorks
Websocket API.

Example Application providing the token directly
================================================

::

   from sparkworksws import SparkWorksWebSocket


   class MyMessageHandler(SparkWorksWebSocket.SparkWorksWebSocketClientProtocol):
       def messageReceived(self, message):
           print message


   if __name__ == '__main__':
       ws = SparkWorksWebSocket(token='your-token', handler=MyMessageHandler)

       ws.start()

Example Application providing credentials
=========================================

::

   import sparkworks_client

   from sparkworksws import SparkWorksWebSocket


   class MyMessageHandler(SparkWorksWebSocket.SparkWorksWebSocketClientProtocol):
       def messageReceived(self, message):
           print message


   if __name__ == '__main__':
       configuration = sparkworks_client.Configuration("username", "password", "client_id", "client_secret")
       ws = SparkWorksWebSocket(configuration=configuration, handler=MyMessageHandler)
       ws.start()
