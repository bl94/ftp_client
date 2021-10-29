from ftplib import FTP
import getpass
import os
import os.path

PATH=os.path.dirname(__file__)#path running file
os.chdir(PATH)#change path into path running file
'''
FTP CLIENT
'''
HOST='testbl.prv.pl'
USER='testbl@prv.pl'
PASSWD="Lepper12"
PORT=21
host1='testftp.ugu.pl'
user2='testftp.ugu.pl'
passwd3="Lepper11"

class Server():
    '''
    class server
    used for communication from a server to client a computer
    '''
    def __init__(self):
        self.host=''
        self.user=''
        self.passwd=''
        self.source=FTP() #variable used to handle a server
        self.login()

    def login(self):
        '''
        login method
        '''
        self.host=input('Enter your ftp address in format xxx.xxx.xxx: ')
        self.user=input('Enter your username: ')
        self.passwd=getpass.getpass('Enter your password: ')
        self.source=FTP(self.host)
        self.source.login(self.user,self.passwd)
        print(f"Connection succesful {self.source.getwelcome()}")

    def action_selection(self):
        """
        method to selecting operations
        """
        print('0.Create new folder\n'
        '1.Remove directory\n'
        '2.Read file\n'
        '3.Write file\n'
        '4.Donwload file from server\n'
        '5.Upload to server\n'
        '6.Listing to dir\n'
        '7.Quit')

        choice=''# variable to store selection
        while choice!='7':
            choice=input('Choose action: ')
            match choice:
                case 0:
                    self.create_new_folder()
                case 1:
                    self.remove_directory()
                case 2:
                    self.read_file(input("Enter the name of the file you want to read"))
                case 3:
                    self.write_file(input("Enter the name of the file you want to write"))
                case 4:
                    self.donwload_file_from_server(input("Enter the name of the file you want\n"
                    "to donwload"))
                case 5:
                    self.upload_to_server(input("Enter the name of the file you want to upload"))
                case 6:
                    self.listdir()
                case 7:
                    self.quit()

    def create_new_folder(self):
        '''
        create new folder on server
        '''
        folder=input("Enter name new folder:")
        self.source.mkd(f'/{folder}')

    def remove_directory(self):
        '''
        create new folder on server
        '''
        folder=input("Enter name new folder or file which you want to delete: ")
        self.source.mkd(f'/{folder}')

    def read_file(self,FILENAME):
        localfile=open(FILENAME,'wb')
        self.source.retrbinary('RETR '+FILENAME,localfile.write)
        localfile.close()
        with open(FILENAME,mode='r',encoding='utf-8')as file:
            print(file.read())
        os.remove(FILENAME)

    def write_file(self,FILENAME):#to change
        localfile=open(FILENAME,'wb')
        self.source.retrbinary('RETR '+FILENAME,localfile.write)
        localfile.close()
        with open(FILENAME,mode='r',encoding='utf-8')as file:
            print(file.read())
        os.remove(FILENAME)

    def donwload_file_from_server(self,FILENAME):
        if os.path.isfile(f'donwload_{FILENAME}'):
            os.remove(f'donwload_{FILENAME}')
        localfile=open(FILENAME,'wb')
        self.source.retrbinary('RETR '+FILENAME,localfile.write)
        localfile.close()
        os.rename('text.txt',f'donwload_{FILENAME}')
 
    def upload_to_server(self,FILENAME):
        localfile=open(FILENAME,mode='rb')
        self.source.storlines('STOR '+ FILENAME,localfile)
        localfile.close()

    def listdir(self):
        print(self.source.dir())

    def quit(self):
        self.source.close()

def __main__():
    ftp_server=Server()

    FILENAME='text.txt'
    ftp_server.donwload_file_from_server(FILENAME)
    ftp_server.upload_to_server('xyz.txt')
    ftp_server.quit()

if __name__=='__main__':
    __main__()
