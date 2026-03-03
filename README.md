# Guide to downloading and running the Rocktutman1 ip-freely scanner

## Description

The **Rocktutman1 scanner** is a ip and port scanner

!! Dont scan networks you arent allowed to since its on some illegal type shi !!

## Requirements

- **Python3** or higher
- *sys*, *re*, *subprocess*, and *socket* modules installed
- Using a linux OS 
- A network to scan

## Instillation 

Clone the git repository

> git clone https://github.com/WTCSC/ip-freely-rocktutman1


## Usage

### Ip scanning

Run file Scanner.py along with the ip address in CIDR notation that you would like to scan the range of

ex:
> python3 Scanner.py 192.168.50.1/24

### Port scanning

Run Scanner.py along with the -p tag, then ports you would like to scan, then the address in CIDR notation 

The -p tag **must come first** and be **immediately** followed by the port number

Ports can be entered as a single port, a comma seperated list, or a range

ex:
> python3 Scanner.py -p 22 192.168.50.1/24 <br>
> python3 Scanner.py -p 22,80,443 192.168.50.1/24 <br>
> python3 Scanner.py -p 0-100 192.168.50.1/24

Note, scanning for ports will drastically increase runtime 

## Configuration

No configuration is curently available

## Running Program

This is what you should see while waiting for the scan
![terminal screen](https://https://github.com/rocktutman1/Porthole/blob/main/images/Running.png)

This is what you should see after
![terminal screen](https://https://github.com/rocktutman1/Porthole/blob/main/images/Output.png)