# pscan
Lightweight Python Port Scanner

## Summary
This tool is a lightweight port scanner which I created for fun, and practice Python programming. This tool is works well in network separated initial systems, or in a machine where you can't pivot.

## Usage

```bash
usage: pscan.py [-h] [-H HOST] [-p PORT] [-t THREADS] [-T TIMEOUT] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -H, --host HOST  	The host of the scan
  -p, --port PORT  	The port (range)
  -t, --threads THREADS	The scanning threads number
  -T, --timeout TIMEOUT The timeout value to wait for the connection
  -o, --output OUTPUT   The output file
  -sT, --scan-tcp       Set the Scan Type to TCP
  -sU, --scan-udp       Set the Scan Type to UDP
```

## Running the Script

```bash
$ python3 pscan.py -H 192.168.0.2 -p 1-10000 -t 100 -o result.txt
```

<u>Example Result</u>

```bash
kali$ python3 pscan.py -H 127.0.0.1 -t 100 -o result.txt
--------------------------------------------------
Scanning Target: 127.0.0.1
Scanning started at:2021-06-08 09:29:01.696293
Total Port(s) Number: 65535
Threads: 100
--------------------------------------------------
22/tcp is open
80/tcp is open
631/tcp is open
34490/tcp is open
43229/tcp is open
                                                  
--------------------------------------------------
Total Scanned Ports Number : 65535
Total Open Ports Number : 5
Closed Ports Number : 65530
Elapsed Time: 0:00:05.154092
--------------------------------------------------

```



**Setting up the ports**

```bash
# Set up port Range between 1-10000
$ python3 pscan.py -H 192.168.0.2 -p 1-10000

# Set up ports 22,53,8080,8000
$ python3 pscan.py -H 192.168.0.2 -p 22,53,8080,8000

# Set up all ports (If no ports specified, the default is all ports)
$ python3 pscan.py -H 192.168.0.2
```



## Future Developement

- Implement UDP scan capabilities
- Implement Host range capabilities
-  Create pscan server which can handle distributed working

