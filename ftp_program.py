'''
FTP CLIENT
'''
import getpass
import os
import os.path
import sys
from ftplib import FTP, error_perm

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
        print('Login to server:\n')
        self.host=input('Enter your ftp address in format xxx.xxx.xxx: ')
        self.user=input('Enter your username: ')
        self.passwd=getpass.getpass('Enter your password: ')
        try:
            self.source=FTP(self.host,timeout=900)
            self.source.login(self.user,self.passwd)
            self.source.set_pasv(True)
            print(f"Connection succesful {self.source.getwelcome()}")
        except error_perm:
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
            '6.Navigate through folder\n'
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
                    self.navigate_ftp_server()
                case '7':
                    self.quit()

    def create_new_folder(self):
        '''
        create new folder on server
        '''
        print("Navigate to directory you want to create the folder")
        self.navigate_ftp_server()
        folder=input("Enter name new folder:")
        self.source.mkd(f'/{folder}')
        print(f"Created new folder '{folder}'\n")

    def remove_directory_or_file(self):
        '''
        remove folder or file on server
        '''
        print("\nNavigate to directory, you want to delete the folder or file:")
        self.navigate_ftp_server()
        try:
            foldername_or_filename=input("\nEnter name folder or file you want to delete: ")
            file_or_dir=self.is_file_or_dir(foldername_or_filename)
            if file_or_dir=='file':
                self.source.delete(f'{foldername_or_filename}')
                print(f"\nDeleted file'{foldername_or_filename}'\n")
            else:
                self.source.rmd(f'{foldername_or_filename}')
                print(f"\nDeleted directory'{foldername_or_filename}'\n")
        except error_perm:
            print("!!!File or folder does not exist!!!")

    def read_file(self):
        '''
        reading file on server(ONLY .txt FILES)
        '''
        print("\nNavigate to directory,you want to read file: ")
        self.navigate_ftp_server()
        try:
            filename=input("\nEnter file name: ")
            print(f"\nRead {filename} file: ")
            with open(filename,'wb')as localfile:
                self.source.retrbinary('RETR '+filename,localfile.write)
            with open(filename,mode='r',encoding='utf-8')as file:
                print(file.read())
            os.remove(filename)
        except error_perm:
            print("!!!File or folder does not exist!!!")

    def write_file(self,filename):#to change
        '''
        writing file on server
        '''
        print("\nNavigate to directory, you want to write file: ")
        self.navigate_ftp_server()
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
        print("\nNavigate to directory,you want to donwload file: ")
        self.navigate_ftp_server()
        try:
            filename=input("Enter the file name you want " \
                        "to donwload:\n")
            if os.path.isfile(f'donwload_{filename}'):
                choice=input("The same file is on your computer folder."\
                "Do you want delete it or rename it? (D or R) ")
                if choice=="D":
                    os.remove(f'donwload_{filename}')
                elif choice=="R":
                    os.rename(f'donwload_{filename}',input("Enter the renamed file :"))
                else:
                    print("\nEnter wrong character\n")
            with open(filename,'wb') as localfile:
                #write file in the same directory, that running file
                self.source.retrbinary('RETR '+filename,localfile.write)
            os.rename(filename,f'donwload_{filename}')
            print(f"\nDonwload 'donwload_{filename}' to client computer\n")
        except error_perm:
            print('*'*50)
            print("\nFile or folder does not exist")
            print('*'*50)

    def upload_file_to_server(self):
        """
        upload file to server
        """
        self.list_files_in_client_computer()
        try:
            filename=input("\nEnter the file name you want "\
                        "to upload: ")
            with open(filename,mode='rb') as localfile:
                self.source.storlines('STOR '+ filename,localfile)
            print(f"\nUpload {filename} to ftp server\n")
        except error_perm:
            print('*'*50)
            print("\nFile or folder does not exist")
            print('*'*50)

    def search_file_in_dir(self,directory,filename):
        """
        search file in directory
        """
        directory=f'/{directory}'
        self.source.cwd(directory)
        list_files=[]
        self.source.retrlines('NLST',list_files.append)
        if filename in list_files:
            return True
        else:
            return False

    def search_folder_in_dir(self,directory):
        """
        search folder in directory
        """
        list_files=[]
        self.source.retrlines('NLST',list_files.append)
        if directory in list_files:
            return True
        else:
            return False

    def is_file_or_dir(self,foldername_or_filename):
        """
        check if a file is a directory or regular file
        """
        list_files_and_folders=[]
        self.source.retrlines('LIST',list_files_and_folders.append)
        for file in list_files_and_folders:
            if foldername_or_filename in file and file.startswith('d'):
                return 'directory'
            elif foldername_or_filename in file:
                return 'file'

    def navigate_ftp_server(self):
        """
        navigate the ftp server
        """
        path='/'
        directory=''
        while directory!='end':
            path+=f"{directory}/"
            print(f"Directory: {path}")
            print("..")
            self.source.cwd(path)
            list_files=[]
            self.source.retrlines('LIST',list_files.append)
            for document in list_files:
                print(f"{document}")
            input_loop=True
            while input_loop:
                directory=input("\nIf you want to navigate through subsequent folders,will enter a 'directory'" \
                "you want to get into\nor if you want to stop navigate through folders, will enter 'end'\n"
                "or if you want to back to the previous directory, will enter 'back': ")
                if self.search_folder_in_dir(directory) and self.is_file_or_dir(directory)=='directory':
                    input_loop=False
                elif directory=='back':
                    input_loop=False
                    path=path.replace(path.rsplit('/',maxsplit=1)[-2],'')
                    directory=''
                elif directory=='end':
                    input_loop=False
                else:
                    print('\n')
                    print('*'*50)
                    print('You enter wrong directory or directory is file. Write correct directory!')
                    print('*'*50)
 
    def list_files_in_client_computer(self):
        '''
        listing files in client computer
        '''
        for file in os.listdir(os.getcwd()):
            if os.path.isdir(file):
                print(f"Package: {os.path.join(os.getcwd(),file)}")
            else:
                print(f"File: {os.path.join(os.getcwd(),file)}")

    def quit(self):
        """
        close connection with server
        """
        print('\nClosed connection with ftp server')
        self.source.close()

def __main__():
    ftp_server=Server()
    ftp_server.action_selection()

if __name__=='__main__':
    PATH=os.getcwd()
    os.chdir(PATH)
    __main__()
