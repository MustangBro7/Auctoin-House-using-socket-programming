import socket
import threading

# Define server host and port
HOST = 'localhost'
PORT = 8080

# Define product details
products = {}
num_products = int(input("Enter number of products: "))
for i in range(num_products):
    name = input(f"Enter name of product {i+1}: ")
    desc = input(f"Enter description of product {i+1}: ")
    start_price = float(input(f"Enter start price of product {i+1}: "))
    products[name] = {'description': desc, 'start_price': start_price, 'highest_bid': start_price, 'highest_bidder': None}

# Define function to handle incoming client connections
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    # Send product details to client
    conn.send(str(num_products).encode())
    for name, details in products.items():
        conn.send(name.encode())
        conn.send(details['description'].encode())
        conn.send(str(details['start_price']).encode())

    # Handle bidding
    while True:
        # Receive bid from client
        data = conn.recv(1024).decode()
        if not data:
            break
        name, bid = data.split(':')
        bid = float(bid)

        # Update product details
        if bid > products[name]['highest_bid']:
            products[name]['highest_bid'] = bid
            products[name]['highest_bidder'] = addr[1]
            # Notify all clients about new highest bid
            for c in clients:
                c.send(f"{name}:{bid}:{addr[1]}".encode())

        # Check if client wants to withdraw
        if bid == -1:
            break

    # Remove client from list of active clients
    clients.remove(conn)
    print(f"[DISCONNECTED] {addr} disconnected.")
    conn.close()

# Create server socket and listen for incoming connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Keep track of active clients
clients = []

print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

# Handle incoming client connections using threading
while True:
    conn, addr = server.accept()
    clients.append(conn)
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
