import socket
import threading

# Define server host and port
HOST = 'localhost'
PORT = 8080

# Define function to handle incoming messages from server
def handle_messages(conn):
    while True:
        # Receive message from server
        data = conn.recv(1024).decode()
        if not data:
            break
        name, bid, bidder = data.split(':')
        if float(bid) > 0:
            print(f"[AUCTION] {name} - Current highest bid: {bid} (Bidder: {bidder})")
        else:
            print(f"[AUCTION] {name} - No bids received yet.")

# Create client socket and connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

num_products = int(client.recv(1024).decode())

# Handle bidding
while True:
    name = input("Enter product name to bid (or 'exit' to quit): ")
    if name == 'exit':
        break
    for i in range(num_products):
        name = client.recv(1024).decode()
        desc = client.recv(1024).decode()
        start_price = float(client.recv(1024).decode())
        print(f"[AUCTION] {name}: {desc} (Start Price: {start_price})")
    if name not in [n.decode() for n in client.recv(1024*num_products).split()]:
        print(f"[ERROR] Invalid product name: {name}")
        continue
    bid = float(input(f"Enter bid for {name}: "))
    client.send(f"{name}:{bid}".encode())

# Receive product details from server



# Send signal to server to indicate client has stopped bidding
client.send('-1'.encode())

# Wait for messages from server to be received and printed
thread = threading.Thread(target=handle_messages, args=(client,))
thread.start()
thread.join()

# Close client socket
client.close()
