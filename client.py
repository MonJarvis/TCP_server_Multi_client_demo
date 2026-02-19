import socket
import threading

class Client:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.client_socket = None
        self.running = False
    
    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")
        self.running = True
    
    def send_data(self, message):
        if self.client_socket:
            data = message.encode('utf-8')
            self.client_socket.send(data)
    
    def receive_messages(self):
        """Continuously listen for messages from server"""
        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if data:
                    message = data.decode('utf-8')
                    print(f"\n{message}")
                    print("You: ", end="", flush=True)  # Restore input prompt
                else:
                    print("\nServer disconnected")
                    self.running = False
                    break
            except:
                if self.running:
                    print("\nConnection error")
                break
    
    def start_conversation(self):
        self.connect()
        
        # Start receiving messages in a separate thread
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        
        print("Type 'quit' to exit\n")
        
        try:
            while self.running:
                # Get message from user
                message = input("You: ")
                
                # Check if user wants to quit
                if message.lower() == 'quit':
                    break
                
                # Send message to server
                self.send_data(message)
                
        except KeyboardInterrupt:
            print("\nDisconnecting...")
        
        self.close_connection()
    
    def close_connection(self):
        self.running = False
        if self.client_socket:
            self.client_socket.close()
            print("Connection closed")

if __name__ == "__main__":
    client = Client()
    try:
        client.start_conversation()
    except Exception as e:
        print(f"Error: {e}")
        client.close_connection()