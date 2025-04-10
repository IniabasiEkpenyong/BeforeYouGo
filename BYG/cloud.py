import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from pathlib import Path
import dotenv

env_path = Path(__file__).resolve().parent / '.env'
dotenv.load_dotenv(env_path)

folder = './images'
tfolder = 'BucketListPics'

def main():

    cloudinary.config(
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key = os.getenv("CLOUDINARY_API_KEY"),
        api_secret = os.getenv("CLOUDINARY_API_SECRET"),
        secure = True
    )
    for filename in os.listdir(folder):
            f = filename.lower();
            if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.avif') :
                file_path = os.path.join(folder, filename)
                public_id = os.path.splitext(filename)[0]
                try:
                    upload_result = cloudinary.uploader.upload(file_path, folder = tfolder,
                                                public_id=public_id)
                    print(upload_result['public_id'])
                    print(retrieve_image(public_id))
                except Exception as e:
                    print (f"Failed to upload {filename} : {e}")

def retrieve_image(public_id):
    try:
        response = cloudinary.api.resource(f"{tfolder}/{public_id}")
        return response.get('url')
    except Exception as e:
        print(f"Failed to retrieve image: {e}")

def add_images_to_database():
    cloudinary.config(
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key = os.getenv("CLOUDINARY_API_KEY"),
        api_secret = os.getenv("CLOUDINARY_API_SECRET"),
        secure = True
    )

    with sqlalchemy.orm.Session(database._engine) as session_db:
        for filename in os.listdir(folder):
                f = filename.lower();
                if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.avif') :
                    item = session_db.query(Bucket).filter(Bucket.cloudinary_id == public_id).first()
                    if item is None:
                        break;
                    else:
                        try:
                            upload_result = cloudinary.uploader.upload(file_path, folder = tfolder,
                                                        public_id=public_id)
                            print(upload_result['public_id'])
                        except Exception as e:
                            print (f"Failed to upload {filename} : {e}")



if __name__ == "__main__":
    main()






    