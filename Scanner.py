import sys, re, subprocess, socket
port_scanning = False

## IDK if we needs comments or not the rubric says we need them but we've never needed them before so ig I do them just to be safe
def pinger(command, results, ip):
    try:
        Up = False
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True, timeout=.5) #runs the ping command
        reply_line = output.splitlines()[1]  
        time_field = reply_line.split()[6] 
        ping_time = time_field.split('=')[1]
        results.append(f"{ip:<15} - Up  ({ping_time}ms)")
        Up = True
    except subprocess.CalledProcessError: #if its down
        results.append(f"{ip:<15} - Down (Unreachable)")
    except subprocess.TimeoutExpired:
        results.append(f"{ip:<15} - Down (Timeout)")
    except Exception:
        results.append(f"Something went wrong reaching {ip}")
    return results, Up

def porter(ip, port, results):
    try:
        with socket.create_connection((ip, port), timeout=.5):
            results.append(f"   - Port {port:<10} Open")
    except Exception:
        results.append(f"   - Port {port:<10} Closed")
    return results

def bar(i, total):
    fraction = i / total
    filled_length = int(30 * fraction)
    bar = '#' * filled_length + ' ' * (30 - filled_length)
    print(f'\r[{bar}] {int(fraction*100)}%', end='')

def er(): #exits if invalid input

    print("Invalid input")
    print("Example input: 'Python3 Scanner.py 192.168.50.1/24'")
    print("Check the README for more details")
    sys.exit(1)

def checkermecker():
    global port_scanning
    if len(sys.argv) < 2: ##Checks if the input is empty and exits if it is
        er()
    else:
        if sys.argv[1] == "-p": #If the user wants port scanning
            if len(sys.argv) != 4:
                er()
            port_scanning = True
            parameter = sys.argv[3]
        else: #If they dont
            if len(sys.argv) != 2:
                er()
            else:
                parameter = sys.argv[1]
    ip_numbers = re.split(r'[./]', parameter)
    if len(ip_numbers) != 5: #Make sure it has 5 'arguements'
        er()
    for x in ip_numbers: #make sure only number
        try: int(x)
        except ValueError:
            er()
    if int(ip_numbers[4]) > 32 or int(ip_numbers[4]) < 0: #make sure subnet mask is between 0-32
        er()
    subnet = ip_numbers[4]
    ip_sect_1 = ip_numbers[0]
    ip_sect_2 = ip_numbers[1]
    ip_sect_3 = ip_numbers[2]
    ip_sect_4 = ip_numbers[3]
    del ip_numbers[4]
    for x in ip_numbers: #Make sure all other number are good
        if int(x) > 255 or int(x) < 0:
            er()
    del ip_numbers
    ip_symbols = re.sub(f"[^{re.escape(".")}{re.escape("/")}]","",parameter)   # get only / and period
    if len(ip_symbols) != 4: er() # Make sure right number of dots and dashes
    if ip_symbols[0] != "." or ip_symbols[1] != "." or ip_symbols[2] != "." or ip_symbols[3] != "/": #make sure stuff is in the right ip_numbersot
        er()
    return subnet, ip_sect_1, ip_sect_2, ip_sect_3, ip_sect_4 

subnet, ip_sect_1, ip_sect_2, ip_sect_3, ip_sect_4 = checkermecker()
var = ''
for i in range(int(subnet)): #Make the octal format
    var += '1'
for i in range(32-len(var)):
    var += '0'
var = int (var,2) #Convert from string to binary
str_binaryaddress = '' #all this stuff converts the actual ip into one big binary number
bin_ip_sect_1 = format(int(ip_sect_1), '08b')
bin_ip_sect_2 = format(int(ip_sect_2), '08b')
bin_ip_sect_3 = format(int(ip_sect_3), '08b')
bin_ip_sect_4 = format(int(ip_sect_4), '08b')
str_binaryaddress = bin_ip_sect_1 + bin_ip_sect_2 + bin_ip_sect_3 + bin_ip_sect_4
bin_binaryaddress = int(str_binaryaddress,2)
starting_address = bin_binaryaddress & var #get the starting address by using binary and
ending_address = starting_address | (~var & 0xffffffff) #get the ending address by using binary or not

all_ips = []
for address in range(starting_address+1, ending_address): #create a list of all ips to ping
    address = format(address, '032b')
    ip = str(int(address[0:8],2)) + "." + str(int(address[8:16],2)) + "." + str(int(address[16:24],2)) + "." + str(int(address[24:32],2)) #put it back into CIDR notation
    all_ips.append(ip)


total = len(all_ips); i = 0 #Defines vaiables for progress bar
results = [f"\nScanned {total} hosts"]
if port_scanning == False: #Scans just ips
    for ip in all_ips:
        command = ['ping', '-c', '1', '-W', '0.5', ip] #makes the command to ping
        results = pinger(command, results, ip)[0]
        bar(i, total)
        i += 1
elif port_scanning == True: #Scans ip and ports
    ports_to_do = sys.argv[2]
    try: ##Checks what type of port input there is
        index_val = ports_to_do.index("-")
    except Exception:
        port_range = False
    else:
        port_range = True
    if port_range == True:
        all_ports = range(int(ports_to_do[:index_val]), int(ports_to_do[index_val+1:])+1)
    else:
        all_ports = ports_to_do.split(",")
    for ip in all_ips:
        command = ['ping', '-c', '1', '-W', '0.5', ip] #makes the command to ping
        results, Up = pinger(command, results, ip)
        if Up:
            for port in all_ports:
                results = porter(ip, int(port), results)
        bar(i, total)
        i += 1

for r in results: #print all the results
    print(r)
            
sys.exit(0) #exit at the end
