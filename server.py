import socket
import threading

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000
clients = []




def handle_client(client_socket, client_address):
    """Handles communication with a connected client."""
    print(f"Connected to {client_address}")
    
    while True:
        try:
            message = client_socket.recv(1024).decode()  # Receive a message
            if not message:
                break  # Disconnect if message is empty
            
            print(f"Received from {client_address}: {message}")

            if message == "userConnect":
                client_socket.send("userConnected".encode())  # Send response

            # Broadcast message to all clients
            for c in clients:
                if c != client_socket:
                    c.send(f"{client_address}: {message}".encode())
                    
        except:
            break  # Handle client disconnection

    print(f"Client {client_address} disconnected")
    client_socket.close()
    clients.remove(client_socket)

def admin_commands():
    """Handles server admin commands in a separate thread."""
    while True:
        cmd = input()
        if cmd == "ADMIN:clear":
            print("Clearing logs...")
        
        if cmd == "ADMIN:stop":
            serverRunning = False

def start_server():
   
    """Starts the server to listen for incoming connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Prevents "Address already in use" error
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

    # Start the admin command listener
    threading.Thread(target=admin_commands, daemon=True).start()

    while True:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

start_server()
