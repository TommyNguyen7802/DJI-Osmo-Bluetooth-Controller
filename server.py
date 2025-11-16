import ftplib
import os

HOST = "us-east-1.sftpcloud.io"
USER = "041ce657031641138ba038bb49625b42"
PASS = "C1C86RSoCkL3LWqCIkSTwOppf9w6rxxu"

filepath = "/Users/osvat0rres/Downloads/sample_video.MP4"
filename = "sample_video.MP4"

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
