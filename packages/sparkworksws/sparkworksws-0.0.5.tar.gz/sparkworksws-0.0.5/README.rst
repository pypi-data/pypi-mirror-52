A client library for accessing live data through the SparkWorks Websocket API.

Example Application
**********************


    from sparkworksws import SparkWorksWebSocket


    class MyMessageHandler(SparkWorksWebSocket.SparkWorksWebSocketClientProtocol):
        def messageReceived(self, message):
            print message


    if __name__ == '__main__':
        ws = SparkWorksWebSocket(token='your-token', handler=MyMessageHandler)
        ws.start()
