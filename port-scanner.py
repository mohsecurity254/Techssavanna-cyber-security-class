import socket
import threading
from queue import Queue
import sys
import argparse

def port_scan(target, port, results_queue):
    """
    Attempt to connect to a specific port and check if it's open
    
    Args:
        target (str): IP address or hostname to scan
        port (int): Port number to check
        results_queue (Queue): Queue to store open port results
    """
    try:
        # Create a new socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a short timeout to make scanning faster
        sock.settimeout(1)
        
        # Attempt to connect to the port
        result = sock.connect_ex((target, port))
        
        # If connection is successful (result == 0), port is open
        if result == 0:
            results_queue.put(port)
        
        # Close the socket
        sock.close()
    except Exception:
        pass

def scan_ports(target, port_range=None):
    """
    Scan a range of ports on the target host
    
    Args:
        target (str): IP address or hostname to scan
        port_range (tuple): Range of ports to scan (start, end)
    
    Returns:
        list: List of open ports
    """
    # Validate target
    try:
        socket.inet_aton(target)
    except socket.error:
        try:
            target = socket.gethostbyname(target)
        except socket.gaierror:
            print(f"Error: Cannot resolve hostname {target}")
            return []

    # Default port range if not specified
    if port_range is None:
        port_range = (1, 1024)
    
    start_port, end_port = port_range
    
    # Queue to store results
    results_queue = Queue()
    
    # List to store threads
    threads = []
    
    # Scan each port in the range
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=port_scan, args=(target, port, results_queue))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Collect results
    open_ports = []
    while not results_queue.empty():
        open_ports.append(results_queue.get())
    
    return sorted(open_ports)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Simple Multithreaded Port Scanner')
    parser.add_argument('target', help='Target IP or hostname to scan')
    parser.add_argument('-p', '--ports', nargs=2, type=int, 
                        metavar=('START', 'END'), 
                        help='Port range to scan (default: 1-1024)')
    
    args = parser.parse_args()
    
    # Determine port range
    port_range = tuple(args.ports) if args.ports else None
    
    print(f"Scanning target: {args.target}")
    
    # Perform port scan
    open_ports = scan_ports(args.target, port_range)
    
    # Display results
    if open_ports:
        print("\nOpen Ports:")
        for port in open_ports:
            try:
                service = socket.getservbyport(port)
                print(f"Port {port}: {service} (Open)")
            except:
                print(f"Port {port}: Unknown Service (Open)")
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
