#!/usr/bin/python3
import socket,os, sys, argparse, queue, threading,time
from datetime import datetime
from enum import Enum


class ScanType(Enum):
    TCP = 1
    UDP = 2
    
class pscan():
    def __init__(self,startport=1,endport=65535,host='127.0.0.1',threads=1,scantype=ScanType.TCP):
        self.start_port = startport
        self.end_port = endport
        self.host = host
        self.thread_num = threads
        self.timeout = .5
        self.open_ports = []
        self.scanned_ports = 0
        self.total_open = 0
        self.total_closed = 0
        self.ports_count = 0
        self.port_queue = queue.Queue()
        self.thread_pool = []
        self.scan_type = scantype
        self.start_time = None
        self.end_time = None
        self.output_file = "output.txt"
        self.write_output = False

   
    def scan(self):
        self.start_time = datetime.now() # Set the scan start time
        self._print_banner() # Print the banner of the Scan
        if self.scan_type == ScanType.TCP:
                for tn in range(self.thread_num):
                    t = threading.Thread(target=self._tcp_scan)
                    self.thread_pool.append(t)
                    t.start()
        else:
            self._udp_scan()
            
        while not self.port_queue.empty():
            self._print_status()
            time.sleep(1)
            
        print(" "*50+"\r")
        # Join for the running threads
        for th in self.thread_pool:
            th.join()        
        self._print_result()
        
        # Write result into a local file
        if self.write_output:
            self._write_output()
            
    def _get_port_range(self,inaddress):
        """
        Get posts in an array from an input string
        if the return array length is 2 it contains a start address and an end address eg.: Range
        else the result cvontains more than 2 items, it contains specific ports, or a single port
        """
        res = []
        if '-' in inaddress:
            p = inaddress.split('-')
            res = p
        elif ',' in inaddress:
            ports = inaddress.split(',')
            res = [int(p) for p in ports if p.isnumeric()] # get all integer from list
        else:
            res = [int(inaddress)]
        return res
    
    def _udp_scan(self):
        print("Not Implemented Yet!")
    def _tcp_scan(self):
        while not self.port_queue.empty():
            port = self.port_queue.get()
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                s.settimeout(self.timeout)
                # returns an error indicator 
                result = s.connect_ex((self.host, port)) 
                if result == 0:
                    print(f"\r{str(port)}/tcp is open")
                    self.total_open += 1
                    self.open_ports.append([port,'tcp'])
                else:
                    #print(name+": Port closed: "+str(port))
                    self.total_closed += 1
                s.close()
                self.scanned_ports += 1
        
            except Exception as x:
                print(x)
                
    def _print_status(self):
        percentage = round((self.scanned_ports / self.ports_count)*100,2)
        print(f"Status: {str(percentage)}%\r",end='')
    def _print_banner(self):
        # Add Banner
        print("-" * 50)
        print("Scanning Target: " + self.host)
        print("Scanning started at:" + str(self.start_time))
        print("Total Port(s) Number: "+str(self.ports_count))
        print("Threads: "+str(self.thread_num))
        print("-" * 50)  
    def _print_result(self):
        self.end_time = datetime.now()
        elapsed = self.end_time - self.start_time
        print()
        print("-" * 50)
        print("Total Scanned Ports Number : "+str(self.scanned_ports))
        print("Total Open Ports Number : "+str(self.total_open))
        print("Closed Ports Number : "+str(self.total_closed))
        print("Elapsed Time: "+str(elapsed))    
        print("-" * 50)
    def _create_output_string(self):
        res = ''
        for o in self.open_ports:
            res += f"{str(o[0])}/{o[1]}\n"
        return res
            
    def _write_output(self):
        ostring = self._create_output_string()   
        with open(self.output_file,'w') as out:
            out.write(ostring)

def parsing_arguments():
    global start_port, end_port, host, thread_num, timeout, namp_scan
    parser = argparse.ArgumentParser()
    parser.add_argument('-H','--host',dest="host",help='The host of the scan')
    parser.add_argument('-p','--port',dest="port",help='The port (range)')
    parser.add_argument('-t','--threads',dest='threads',help='The scanning threads number')
    parser.add_argument('-T','--timeout',dest='timeout',help='The timeout value to wait for the connection')
    parser.add_argument('-o','--output',dest='output',help='The output file')
    parser.add_argument('-sT','--scan-tcp',dest='scantcp', action='store_true',help='Set the Scan Type to TCP')
    parser.add_argument('-sU','--scan-udp',dest='scanudp', action='store_true',help='Set the Scan Type to UDP')  
    
    args = parser.parse_args()
    return args


        
def main():
    scanner = pscan()
    args = parsing_arguments()
    # parse given arguments
    if args.host: 
        scanner.host = args.host
    else:
        print("[!] Missing target host!")
        sys.exit(1)        
    if args.threads: scanner.thread_num = int(args.threads)
    else:
        scanner.thread_num = 1
    if args.timeout: scanner.timeout = int(args.timeout)
    # Parse the port range
    if args.port:
        r = scanner._get_port_range(args.port)
        if len(r) == 1:
            scanner.start_port = int(r[0])
            scanner.end_port = int(r[0])
            scanner.port_queue.put(scanner.start_port)
            scanner.ports_count = 1
        elif len(r) == 2:
            scanner.start_port = int(r[0])
            scanner.end_port = int(r[1])
            for p in range(scanner.start_port,scanner.end_port+1):
                scanner.port_queue.put(p)
            scanner.ports_count = scanner.port_queue.qsize()
            
        elif len(r) > 2:
            for p in r:
                scanner.port_queue.put(p)
            scanner.ports_count = scanner.port_queue.qsize()
    else:
        for p in range(scanner.start_port,scanner.end_port+1):
            scanner.port_queue.put(p)
            scanner.ports_count = scanner.port_queue.qsize()
            
    if scanner.ports_count > 1:
        # If more threads than scanned ports, decrease the threads number to the number of the ports
        if scanner.end_port-scanner.start_port < scanner.thread_num: scanner.thread_num = scanner.end_port - scanner.start_port
                
    if args.scantcp:
        scanner.scan_type = ScanType.TCP
        if args.scanudp: print("Only one Scan Type can set! Exit!"); sys.exit(1) 
    if args.scanudp:
        scanner.scan_type = ScanType.UDP
        if args.scantcp: print("Only one Scan Type can set! Exit!"); sys.exit(1)
    if args.output: 
        scanner.output_file = args.output
        scanner.write_output = True
            
    # Run the scanner instance
    scanner.scan()
    
if __name__ == '__main__':
    main()
