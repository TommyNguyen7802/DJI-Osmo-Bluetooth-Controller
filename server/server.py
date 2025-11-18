import ftplib
import os

HOST = "Host name"
USER = "Username"
PASS = "Password of the server"

filepath = "Path of the file"
filename = "Nanme of the file"

if not os.path.exists(filepath):
    print(f"File not found: {filepath}")
else:
    try:
        print(f"Connecting to {HOST}...")
        with ftplib.FTP(HOST) as ftp:
            ftp.login(USER, PASS)
            ftp.encoding = "utf-8"
            print("Logged in successfully.")
            # Upload file
            with open(filepath, "rb") as file:
                print(f"Uploading '{filepath}'...")
                ftp.storbinary(f"STOR {os.path.basename(filepath)}", file)
                print("Upload complete!")

            # List files on server
            print("\nFiles on server:")
            ftp.dir()

            # Download the same file
            download_name = "downloaded_" + filename
            with open(download_name, "wb") as file:
                print(f"\nDownloading '{filename}' as '{download_name}'...")
                ftp.retrbinary(f"RETR {filename}", file.write)
                print("Download complete!")

            # Display the contents of the downloaded file
            with open(download_name, "r", encoding="utf-8") as file:
                print("\nFile contents:\n" + file.read())

            # Close connection explicitly (optional since 'with' handles it)
            ftp.quit()

    except ftplib.all_errors as e:
        print(f"FTP error: {e}")
