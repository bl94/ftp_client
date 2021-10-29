'''
FTP CLIENT
'''
from ftplib import FTP
import getpass
import os
import os.path

PATH=os.path.dirname(__file__)#path running file
os.chdir(PATH)#change path into path running file

HOST='testbl.prv.pl'
USER='testbl@prv.pl'
PASSWD="Lepper12"
PORT=21
HOST2='testftp.ugu.pl'
USER2='testftp.ugu.pl'
PASSWD="Lepper11"

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
        self.host='testftp.ugu.pl'
        self.user='testftp.ugu.pl'
        self.passwd="Lepper11"
       #self.host=input('Enter your ftp address in format xxx.xxx.xxx: ')
       #self.user=input('Enter your username: ')
       #self.passwd=getpass.getpass('Enter your password: ')
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
                    self.donwload_file_from_server(input("Enter the name of the file you want"\
                    "to donwload"))
                case 5:
                    self.upload_file_to_server(input("Enter the name of the file you want to upload"))
                case 6:
                    self.list_dir()
                case 7:
                    self.quit()

    def create_new_folder(self):
        '''
        create new folder on server
        '''
        folder=input("Enter name new folder:")
        self.source.mkd(f'/{folder}')
        print(f"Created new folder '{folder}'")

    def remove_directory(self):
        '''
        create new folder on server
        '''
        folder=input("Enter name folder or file you want to delete: ")
        self.source.mkd(f'/{folder}')
        print(f"Deleted folder '{folder}'")
    
    def is_file_in_dir(self):
        list_files=[]
        self.source.retrlines('NLST',list_files.append)
        return list_files

    def read_file(self,FILENAME):
        '''
        reading file on server(ONLY .txt FILES)
        '''
        print(f"Read{FILENAME} file : ")
        with open(FILENAME,'wb')as localfile:
            self.source.retrbinary('RETR '+FILENAME,localfile.write)
        with open(FILENAME,mode='r',encoding='utf-8')as file:
            print(file.read())
        os.remove(FILENAME)
        
    def write_file(self,FILENAME):#to change
        '''
        writing file on server
        '''
        localfile=open(FILENAME,'wb')
        self.source.retrbinary('RETR '+FILENAME,localfile.write)
        localfile.close()
        with open(FILENAME,mode='r',encoding='utf-8')as file:
            print(file.read())
        os.remove(FILENAME)

    def donwload_file_from_server(self,FILENAME):
        '''
        donwload file on server
        '''
        #if There is the same file on client computer folder and on server
        #we have two solutions, we can change name file or remove file on client computer
        if os.path.isfile(f'donwload_{FILENAME}'):
            try:
                choice=input("The same file is on your computer folder. Do you want delete it or rename it? (D or R)" )
                if choice=="D":#
                    os.remove(f'donwload_{FILENAME}')
                if choice=="R":
                    os.rename(f'donwload_{FILENAME}',input("Enter the renamed file :"))
            except TypeError:
                print("Enter wrong character")
        with open(FILENAME,'wb') as localfile:
            self.source.retrbinary('RETR '+FILENAME,localfile.write) #write file in the same directory that running file
        os.rename(FILENAME,f'donwload_{FILENAME}')
        print(f"Donwload f'donwload_{FILENAME}' to client computer")
 
    def upload_file_to_server(self,FILENAME):
        """
        upload file to server
        """
        with open(FILENAME,mode='rb') as localfile:
            self.source.storlines('STOR '+ FILENAME,localfile)
        print(f"Upload {FILENAME} to server")

    def list_dir(self):
        """
        listing file in directory
        """
        dirname=input("Enter directory which you want listing files or if you want listing files from main path enter '/': ")
        dirname=f'/{dirname}'
        self.source.cwd(dirname)
        list_files=[]
        self.source.retrlines('NLST',list_files.append)
        return list_files

    def quit(self):
        """
        close connection with server
        """
        print('Closed connection with server')
        self.source.close()

def __main__():
    ftp_server=Server()
    print(ftp_server.is_file_in_dir())
    print(ftp_server.list_dir())
    #ftp_server.donwload_file_from_server(FILENAME)
    #ftp_server.upload_fileto_server('xyz.txt')
    #ftp_server.quit()

if __name__=='__main__':
    __main__()
