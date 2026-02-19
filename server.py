import socket
import threading

class Server:
    def __init__(self, host='localhost', port=12345, max_clients=5):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(max_clients)
        self.clients = []  # List to store all connected clients
    
    def accept_clients(self):
        print("Server is listening for connections...")
        client_socket, address = self.server_socket.accept()
        print(f"Connection from {address} has been established.")
        
        # Add client to our list
        client_info = {'socket': client_socket, 'address': address}
        self.clients.append(client_info)
        print(f"Total clients connected: {len(self.clients)}")
        
        return client_socket, address

    def receive_data(self, client_socket):
        # Placeholder for receiving data from the client
        data = client_socket.recv(1024)
        if data:
            message = data.decode('utf-8')
            print(f"Received message: {message}")
            return message
        else:
            print("Client disconnected")
            return None

    def send_data(self, client_socket, message):
        # Placeholder for sending data to the client
        data = message.encode('utf-8')
        client_socket.send(data)

    def broadcast_message(self, message, sender_address=None):
        """Send a message to all connected clients"""
        print(f"Broadcasting: {message}")
        disconnected_clients = []
        
        for client_info in self.clients:
            try:
                # Don't send message back to the sender (optional)
                if sender_address and client_info['address'] == sender_address:
                    continue
                    
                self.send_data(client_info['socket'], message)
            except:
                # Client disconnected, mark for removal
                disconnected_clients.append(client_info)
        
        # Remove disconnected clients
        for client_info in disconnected_clients:
            self.remove_client(client_info)

    def remove_client(self, client_info):
        """Remove a client from the list"""
        if client_info in self.clients:
            self.clients.remove(client_info)
            print(f"Removed client {client_info['address']}. Total clients: {len(self.clients)}")

    def send_current_users(self, new_client_socket):
        """Send list of currently connected users to new client"""
        if len(self.clients) > 1:  # More than just the new client
            user_list = []
            for client_info in self.clients:
                if client_info['socket'] != new_client_socket:  # Don't include the new client
                    user_list.append(str(client_info['address']))
            
            if user_list:
                users_msg = f"📋 Currently online: {', '.join(user_list)}"
                self.send_data(new_client_socket, users_msg)
        else:
            self.send_data(new_client_socket, "📋 You are the first user online!")

    def handle_client(self, client_socket, address):
        """Handle communication with one specific client"""
        print(f"Starting conversation with {address}")
        
        # Send current user list to new client
        self.send_current_users(client_socket)
        
        # Send welcome message to everyone ELSE (not the new client)
        self.broadcast_message(f"🟢 {address} joined the server!", sender_address=address)
        
        try:
            while True:
                # Receive message from client
                message = self.receive_data(client_socket)
                
                # If no message (client disconnected), break
                if message is None:
                    break
                
                # Broadcast the message to all other clients
                broadcast_msg = f"{address}: {message}"
                self.broadcast_message(broadcast_msg, sender_address=address)
                
        except Exception as e:
            print(f"Error with client {address}: {e}")
        finally:
            # Remove client and notify others
            client_info = {'socket': client_socket, 'address': address}
            self.remove_client(client_info)
            self.broadcast_message(f"🔴 {address} left the server")
            
            print(f"Conversation with {address} ended")
            client_socket.close()

if __name__ == "__main__":
    server = Server()
    print("Server can now handle multiple clients!")
    
    try:
        while True:
            # Accept a client
            client_socket, address = server.accept_clients()
            
            # Start a new thread to handle this client
            client_thread = threading.Thread(
                target=server.handle_client, 
                args=(client_socket, address),
                daemon=True  # Thread will close when main program closes
            )
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        server.server_socket.close()    
