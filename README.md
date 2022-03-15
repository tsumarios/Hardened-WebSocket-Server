# Hardened-WebSocket-Server

Simple PoC about adding a ticket-based authentication layer in a WebSocket server.

The WS client sends its authentication token to the WS server as first message after the handshake. The WS server then validates the auth proof (in this case by simulating a request to a third-party auth server) and keeps/terminates the WS connection accordingly. The schema below illustrates the ticket-based authentication mechanism within the WebSocket protocol:

![WS Ticket-Based Auth](/img/ws_ticket-based_auth.png)

This demo is part of the "WebSocket (In)Security and Authentication" articles (written in Italian) available at <https://blog.rev3rse.it/> TODO: link.

## Dependencies

This PoC is implemented using the [SimpleWebSocketServer](https://github.com/dpallot/simple-websocket-server/blob/master/SimpleWebSocketServer/SimpleWebSocketServer.py) module.

## Usage

In order to run the proof-of-concept, clone this repository and install the requirements by opening your favourite **Terminal**, typing as follows:

```sh
git clone https://github.com/tsumarios/Hardened-WebSocket-Server
cd Hardened-WebSocket-Server
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Then, you can run the HTTP server within the WebSocket server by typing the following command:

```sh
python3 ws_server.py TODO: parameters
```

Note that by default the HTTP server will be listening on port 80 (or 443 if using HTTPS) and the WebSocket server will be using port 5678. The arguments are referring to the WebSocket server.

Eventually, you can open your favourite browser and go at <http://localhost/> (or <https://localhost/> if using TLS) and open the ws.html (or wss.html) file to interact with the WS server.

#### TLS

The WebSocket server can also run using the WSS (WebSocket Secure) protocol. Assuming the certificate and private key are in the base directory and named as "cert.pem" and "key.pem" - these are the default values for the arguments -, just run the script as follows:

```sh
python3 ws_server.py --ssl
```

If the TLS protocol is enabled, remember to open the wss.html file instead of the ws.html page. Alternatively, if you are using another WebSocket client, remember to switch the WebSocket URL from <ws://host:port/> to <wss://host:port/>.

#### Contacts

- Email: marioraciti@pm.me
- LinkedIn: linkedin.com/in/marioraciti
- Twitter: twitter.com/tsumarios

**Enjoy WebSockets!**
