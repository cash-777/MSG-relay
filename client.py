import socket
import threading

def receive_messages():
    """Listens for incoming messages from the server."""
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            print("\nServer:", message)
        except:
            print("\nDisconnected from server.")
            break

def try_user_connect():
    """Attempts to connect to the server and send a connection message."""
    try:
        client.connect((ip, port))
        client.send("userConnect".encode())
        response = client.recv(1024).decode()
        print("Server:", response)
    except:
        print("Failed to connect to server.")
        exit()

# User input for connection details
uname = input("Enter username: ")
ip = input("Enter IP address: ")
port = int(input("Enter port: "))

print("Starting socket...")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting to server...")
try_user_connect()

# Start receiving messages in a separate thread
threading.Thread(target=receive_messages, daemon=True).start()

# Main loop for sending messages
while True:
    userInput = input("Enter message: ")

    if userInput == "/exit":
        break
    
    elif userInput == "/panic":
        client.send(f"CLIENT: USER {uname} HAS REQUESTED SERVER WIPE".encode())
    else:
        message = uname + ": " + userInput
        client.send(message.encode())

client.close()
print("Disconnected.")
