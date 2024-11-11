import socket #connect to ports
import threading #for multiple workloads
#import sys
from queue import Queue #This imports all the classes from the queue module
from termcolor import colored  # Make sure to install termcolor: pip install termcolor

open_ports = []# List to store open ports

ps_intro = '''


/$$$$$$$                       /$$            /$$$$$$                                                             
| $$__  $$                     | $$           /$$__  $$                                                            
| $$  \ $$ /$$$$$$   /$$$$$$  /$$$$$$        | $$  \__/  /$$$$$$$  /$$$$$$  /$$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$ 
| $$$$$$$//$$__  $$ /$$__  $$|_  $$_/        |  $$$$$$  /$$_____/ |____  $$| $$__  $$| $$__  $$ /$$__  $$ /$$__  $$
| $$____/| $$  \ $$| $$  \__/  | $$           \____  $$| $$        /$$$$$$$| $$  \ $$| $$  \ $$| $$$$$$$$| $$  \__/
| $$     | $$  | $$| $$        | $$ /$$       /$$  \ $$| $$       /$$__  $$| $$  | $$| $$  | $$| $$_____/| $$      
| $$     |  $$$$$$/| $$        |  $$$$/      |  $$$$$$/|  $$$$$$$|  $$$$$$$| $$  | $$| $$  | $$|  $$$$$$$| $$      
|__/      \______/ |__/         \___/         \______/  \_______/ \_______/|__/  |__/|__/  |__/ \_______/|__/      
                                                                                                                   
                                                                                                                   
                                                                                                                   
'''


def confirm_execution():# port scanners are illegal to be used without permission, therefore We have to ask the user to confirm the execution of such code.
    print(ps_intro)
    confirmation = input("WARNING! Do not use unless you have permission!\nAre you sure you want to proceed? (yes/no): ").strip().lower()
    return confirmation == "yes"

def port_scan(target, port):# Function to scan a single port
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Create a TCP socket
        sock.settimeout(1)# Set timeout to 1 second
        result = sock.connect_ex((target, port))# Attempt to connect to the target and port
        if result == 0:# Check if connection was successful
            print(colored(f"Port {port} is open", "green"))# If successful, print that the port is open and add it to the open_ports list USING  / F STRING TO SAVE SPACE
            open_ports.append(port)
        else:
            print(colored(f"Port {port} is closed", "red"))# If not successful, print that the port is closed
        sock.close()# Close the socket
    except Exception as e:
        print(colored(f"Error scanning port {port}: {e}", "red"))# If an exception occurs during scanning, print the error

def port_scan_worker(target, port_queue):# Worker function for port scanning
    while not port_queue.empty():# Loop until all ports in the queue are scanned
        port = port_queue.get()# Get the next port from the queue
        port_scan(target, port)# Scan the port
        port_queue.task_done()# Mark the task as done

def main():# Main function

    if confirm_execution():
        pass
    else:
        print("Execution aborted.")
        exit()

    target = input("Enter target host: ")# Get target host from user input
    start_port = int(input("Enter starting port: "))# Get starting port from user input
    end_port = int(input("Enter ending port: "))# Get ending port from user input

    if end_port < start_port:# Validate port range
        print("Ending port cannot be less than starting port.")
        sys.exit(1)

    port_queue = Queue()# Create a queue to hold ports to be scanned

    for port in range(start_port, end_port + 1):# Enqueue ports to be scanned
        port_queue.put(port)

    num_threads = min(100, end_port - start_port + 1)# Determine the number of threads to use (limited to 100)

    for _ in range(num_threads):# Start worker threads for port scanning
        thread = threading.Thread(target=port_scan_worker, args=(target, port_queue))
        thread.start()

    port_queue.join()# Wait for all threads to finish

    print("\n--- Summary ---")# Print summary of the scan with colors
    print(colored(f"Total ports scanned: {end_port - start_port + 1}", "blue"))
    print(colored(f"Open ports: {len(open_ports)}", "blue"))
    if open_ports:
        print(colored("Open ports: ", "blue") + colored(', '.join(map(str, open_ports)), "green"))

if __name__ == "__main__": #prevents file being imported as module.The if name equals main block guards the print statement, to ensure it executes only when the file is intentionally run directly as a script or application.
    main()