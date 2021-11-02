'''
FTP CLIENT
'''
from ftplib import FTP
import getpass
import os
import os.path
import sys

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
        try:
            self.source=FTP(self.host,timeout=900)
            self.source.login(self.user,self.passwd)
            self.source.set_pasv(True)
            print(f"Connection succesful {self.source.getwelcome()}")
        except:
            print('Error connecting to FTP server')
            sys.exit()

    def action_selection(self):
        """
        method to selecting operations
        """
        choice=''#variable to store choice
        while choice!='7':
            print('\n0.Create new folder\n'
            '1.Remove directory\n'
            '2.Read file\n'
            '3.Write file\n'
            '4.Donwload file from server\n'
            '5.Upload to server\n'
            '6.Listing to dir\n'
            '7.Quit\n')

            choice=input('Choose action: ')
            match choice:
                case '0':
                    self.create_new_folder()
                case '1':
                    self.remove_directory_or_file()
                case '2':
                    self.read_file()
                case '3':
                    self.write_file(input("Enter the name of the file you want to write: "))
                case '4':
                    self.donwload_file_from_server()
                case '5':
                    self.upload_file_to_server()
                case '6':
                    self.list_dir(input("Enter the directory from you want" \
                    "to get list file,if you want to get list file from main path, enter '/':"))
                case '7':
                    self.quit()

    def create_new_folder(self):
        '''
        create new folder on server
        '''
        folder=input("Enter name new folder:")
        self.source.mkd(f'/{folder}')
        print(f"Created new folder '{folder}'\n")

    def remove_directory_or_file(self):
        '''
        remove folder or file on server
        '''
        self.list_dir()
        directory=input("Enter the directory from you want "\
                    "to delete, if you want to delete from main path, enter '/' : ")
        self.list_dir(directory)
        foldername_or_filename=input("Enter name folder or file you want to delete: ")
        file_or_dir=self.is_file_or_dir(directory,foldername_or_filename)
        if file_or_dir=='file':
            self.source.delete(f'{foldername_or_filename}')
            print(f"\nDeleted file'{foldername_or_filename}'\n")
        else:
            self.source.rmd(f'{foldername_or_filename}')
            print(f"\nDeleted directory'{foldername_or_filename}'\n")

    def read_file(self):
        '''
        reading file on server(ONLY .txt FILES)
        '''
        self.list_dir()
        directory=input("Enter directory file who want to read or " \
         "if you want to read file from main path, enter '/': ")
        directory=f'/{directory}'
        self.source.cwd(directory)
        filename=input("Enter file name: ")
        is_file_in_dir=self.search_file_in_dir(directory,filename)
        if is_file_in_dir:
            print(f"Read {filename} file:\n ")
            with open(filename,'wb')as localfile:
                self.source.retrbinary('RETR '+filename,localfile.write)
            with open(filename,mode='r',encoding='utf-8')as file:
                print(file.read())
            os.remove(filename)
        else:
            print("\nError in your file name or wrong file path\n")

    def write_file(self,filename):#to change
        '''
        writing file on server
        '''
        localfile=open(filename,'wb')
        self.source.retrbinary('RETR '+filename,localfile.write)
        localfile.close()
        with open(filename,mode='r',encoding='utf-8')as file:
            print(file.read())
        os.remove(filename)

    def donwload_file_from_server(self):
        '''
        donwload file on server
        '''
        #if There is the same file on client computer folder and on server
        #we have two solutions, we can change name file or remove file on client computer
        self.list_dir()
        directory=input("Enter the directory from you want " \
                    "to donwload: ")
        filename=input("Enter the file name you want" \
                    "to donwload:\n ")
        is_file_in_dir=self.search_file_in_dir(directory,filename)
        if is_file_in_dir:
            if os.path.isfile(f'donwload_{filename}'):
                try:
                    choice=input("The same file is on your computer folder."\
                    "Do you want delete it or rename it? (D or R) ")
                    if choice=="D":
                        os.remove(f'donwload_{filename}')
                    if choice=="R":
                        os.rename(f'donwload_{filename}',input("Enter the renamed file :"))
                except TypeError:
                    print("Enter wrong character")
            with open(filename,'wb') as localfile:
                #write file in the same directory that running file
                self.source.retrbinary('RETR '+filename,localfile.write)
            os.rename(filename,f'donwload_{filename}')
            print(f"Donwload 'donwload_{filename}' to client computer")
        else:
            print("Error in your file name or wrong file path")

    def upload_file_to_server(self):
        """
        upload file to server
        """
        filename=input("Enter the file name you want " \
                    "to upload:\n ")
        with open(filename,mode='rb') as localfile:
            self.source.storlines('STOR '+ filename,localfile)
        print(f"Upload {filename} to server")

    def search_file_in_dir(self,directory,filename):
        """
        search file in directory
        """
        directory=f'/{directory}'
        self.source.cwd(directory)
        list_files=[]
        self.source.retrlines('NLST',list_files.append)
        self.list_dir(directory)
        if filename in list_files:
            return True
        else:
            return False

    def is_file_or_dir(self,directory,foldername_or_filename):
        """
        check if a file is a directory or regular file
        """
        self.source.cwd(f'/{directory}')
        list_files_and_folders=[]
        self.source.retrlines('LIST',list_files_and_folders.append)
        for file in list_files_and_folders:
            if foldername_or_filename in file and file.startswith('d'):
                return 'directory'
            elif foldername_or_filename in file:
                return 'file'

    def list_dir(self,directory='/'):
        """
        get list file in directory
        """
        directory=f'/{directory}'
        self.source.cwd(directory)
        list_files=[]
        self.source.retrlines('LIST',list_files.append)
        print(directory)
        for document in list_files:
            print(f"{document}")

    def navigate(self):
        """
        navigate the ftp server
        """
        path='/'
        directory=''
        while directory!='end':
            path+=directory
            self.source.cwd(path)
            list_files=[]
            self.source.retrlines('LIST',list_files.append)
            print(directory)
            for document in list_files:
                print(f"{document}")
            directory=input("\nIf you want to navigate through subsequent folders,enter a directory name" \
            "you want to get into\n or if you want to stop navigate through folders, enter 'end'\n"
            "or if you want to back to the previous directory, enter 'back': ")
            if directory=='back':
                path=path.replace(path.rsplit('/',maxsplit=1)[-1],'')
                directory=''

    def quit(self):
        """
        close connection with server
        """
        print('Closed connection with server')
        self.source.close()

def __main__():
    PATH=os.getcwd()
    os.chdir(PATH)
    ftp_server=Server()
    ftp_server.navigate()
    #ftp_server.action_selection()
if __name__=='__main__':
    __main__()
