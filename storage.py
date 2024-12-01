import os
from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth) 