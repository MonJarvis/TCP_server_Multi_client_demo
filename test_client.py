import socket

def test_connection():
    try:
        # Create client socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to server
        print("Attempting to connect...")
        client.connect(('localhost', 12345))
        print("Connected to server!")
        
        # Connection will be closed immediately by server
        
        print("Connection closed")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()