import socket
import threading
import sys
import pickle

MENU_OPTION = ['ls', 'create', 'delete', 'upload', 'download', 'drop', 'exit', 'help']

class Cliente():
  def __init__(self, host, port):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((host, port))

    message_recive = threading.Thread(target=self.message_recive)
    message_recive.daemon = True
    message_recive.start()

    self.download_path = ''

    while True:
      command = input('>').split()
      if command[0] in MENU_OPTION:
        if command[0] != 'exit':
          if command[0] == 'help':
            self.help()
          if command[0] == 'upload':
            command = self.upload(command)
            if not command:
              continue
          if command[0] == 'download':
            self.download_path = command[2]
          self.send_command(command)
        else: 
          self.socket.close()
          sys.exit()
      else:
        print('Invalid option, try againg or use "help" to show commands')
  
  def message_recive(self):
    while True:
      try:
        data = self.socket.recv(1024)
        recive = pickle.loads(data)
        print(recive) if not self.download(recive) else None
      except:
        pass
  
  def send_command(self, command):
    self.socket.send(pickle.dumps(command))

  def upload(self, command):
    if len(command) == 3:
      with open(command[2], 'rb') as file:
        command.append({ "name": command[2].split('\\')[-1], "data": file.readlines() })
        return command
    elif len(command) < 3:
      print('Missing arguments')
    else:
      print('Extra arguments')
    return False

  def download(self, recive):
    if isinstance(recive, dict):
      with open(f'{self.download_path}/{recive["name"]}', 'wb') as file:
        file.writelines(recive["data"])
        self.download_path = ''
        return True
    return False


  def help(self):
    print('''
    ls <nameBucket>                       List yours buckets and files
    create <nameBucket>                   Create a new bucket
    delete <nameBucket>                   Delete a specific bucket
    upload <bucketName> <fullFilePath>    Upload file to bucket
    download <bucketPath> <downloadPath>  Download file from bucket
    drop <bucketPath>                     Drop file from bucket
    help                                  Show this menu
    exit                                  Close connection
    ''')

if __name__ == '__main__':
  host, port = sys.argv[1:] if len(sys.argv) == 3 else ['localhost', 4000]
  print('Missing Arguments, default configuration activate') if len(sys.argv) > 1 and len(sys.argv) < 3 else None
  Cliente(host, int(port))