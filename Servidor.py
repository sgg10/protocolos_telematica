import socket
import threading
import sys
import pickle
import os
import shutil

class Servidor():
  def __init__(self, host='localhost', port=4000, bucketLocation = ''):
    self.clients = []
    self.bucketLocation = bucketLocation + "/" if bucketLocation else ""
    self.createBucket(f'{self.bucketLocation}Clients')
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind((host, port))
    self.socket.listen(10)
    self.socket.setblocking(False)

    accept = threading.Thread(target=self.accept_connection)
    process = threading.Thread(target=self.process_connection)

    accept.daemon = True
    process.daemon = True

    accept.start()
    process.start()

    while True:
      message = input('>')
      if message == 'exit':
        self.socket.close()
        sys.exit()

  def executeAction(self, data, Actualclient):
    for client in self.clients:
      try:
        if client[0] == Actualclient[0]:
          if data[0] == 'ls':
            self.send_message(Actualclient[0], self.list(f'{self.bucketLocation}Clients/{Actualclient[1][1]}/{data[1] if len(data) > 1 else ""}'))
          elif data[0] == 'create':
            self.create_command(Actualclient, data)
          elif data[0] == 'delete':
            self.delete_command(Actualclient, data)
          elif data[0] == 'upload':
            self.upload_command(Actualclient, data)
          elif data[0] == 'download':
            self.download_command(Actualclient, data)
          elif data[0] == 'drop':
            self.drop_command(Actualclient, data)
        else:
          continue
      except:
        continue

  def create_command(self, Actualclient, data):
    if len(data) > 1:
      if data[1] not in self.list(f'{self.bucketLocation}Clients/'.replace('/', '\\')):
        self.createBucket(f'{self.url(Actualclient, data)}'.replace('/', '\\'))
        self.send_message(Actualclient[0], f'{data[1]} was created')
      else:
        self.send_message(Actualclient[0], f'{data[1]} alredy exists')
    else:
      self.send_message(Actualclient[0], "You don't create a bucket without name")
  
  def delete_command(self, Actualclient, data):
    if len(data) > 1:
      self.deleteBucket(f'{self.url(Actualclient, data)}'.replace('/', '\\'))
      self.send_message(Actualclient[0], f'{data[1]} was deleted')
    else:
      self.send_message(Actualclient[0], "You don't delete a bucket without name")

  def upload_command(self, Actualclient, data):
    with open(f'{self.url(Actualclient, data)}/{data[3]["name"]}.SGG'.replace('/', '\\'), 'wb') as file:
      pickle.dump(data[3], file)
      self.send_message(Actualclient[0], f'{data[3]["name"]} was create')

  def download_command(self, Actualclient, data):
    with open(f'{self.url(Actualclient, data)}.SGG'.replace('/', '\\'), 'rb') as file:
      file_data = pickle.load(file)
      self.send_message(Actualclient[0], dict(file_data))

  def drop_command(self, Actualclient, data):
    self.deleteFile(f'{self.pwd() + "/" if not self.bucketLocation else "" }{self.url(Actualclient, data)}.SGG'.replace('/', '\\'))
    self.send_message(Actualclient[0], 'File was deleted')

  def send_message(self, client, message):
    client.send(pickle.dumps(message))

  def url(self, Actualclient, data):
    return f'{self.bucketLocation}Clients/{Actualclient[1][1]}/{data[1]}'

  def accept_connection(self):
    print('Accepting connection')
    while True:
      try:
        conn, address = self.socket.accept()
        conn.setblocking(False)
        self.createBucket(f'{self.bucketLocation}Clients/{address[1]}'.replace('/', '\\'))
        self.clients.append((conn, address))
      except:
        pass

  def process_connection(self):
    print('Processing connection')
    while True:
      if len(self.clients) > 0:
        for client in self.clients:
          try:
            data = pickle.loads(client[0].recv(1024))
            self.executeAction(data, client) if data != None else None
          except:
            pass
  
  def createBucket(self, name):
    try:
      os.mkdir(name)
      return True
    except OSError as OSe:
      return OSe.filename, OSe.strerror

  def deleteBucket(self, bucketName):
    try:
      shutil.rmtree(bucketName)
      return True
    except OSError as OSe:
      print(f'Error: {OSe.filename} - {OSe.strerror}')

  def deleteFile(self, fileName):
    try:
      os.remove(fileName)
      return True
    except OSError as OSe:
      print(f'Error: {OSe.filename} - {OSe.strerror}')
      return False

  def list(self, address):
    try:
      l = os.listdir(address)
      for i in range(len(l)):
        l[i] = l[i].replace('.SGG', '')
      return l
    except OSError as OSe:
      print(f'Error: {OSe.filename} - {OSe.strerror}')
      return False

  def pwd(self):
    return os.getcwd()

if __name__ == '__main__':
  host, port, bucketLocation = sys.argv[1:] if len(sys.argv) == 4 else ['localhost', 4000, '']
  print('Missing Arguments, default configuration activate') if len(sys.argv) > 1 and len(sys.argv) < 4 else None
  Servidor(host, int(port), bucketLocation)