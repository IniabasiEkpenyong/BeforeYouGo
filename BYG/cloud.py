
from dotenv import load_dotenv

import cloudinary

import os

load_dotenv()

cloudinary.config(
    cloud_name = os.getenv("doydyfm1q"),
    api_key = os.getenv("979955127449654"),
    api_secret = os.getenv("yhoJbwpg-jq1zmYduxmElcp_LOg"),
    secure = True
)

folder = ['./images']
tfolder = ['BucketListPics']
for filename in os.listdir(folder):
        if filename.lower().endswith('.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif') :
            file_path = os.path.join(folder, filename)
            public_id = os.path.splittext(filename)[0]
            try:
                upload_result = cloudinary.uploader.upload(file_path,folder = tfolder,
                                            public_id=public_id)
                print(upload_result['public_id'])
            except Exception as e:
                print (f"Failed to upload {filename} : {e}")







    