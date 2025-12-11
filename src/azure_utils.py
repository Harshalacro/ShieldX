import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables (for local testing)
load_dotenv()

def get_blob_service_client():
    """
    Returns a BlobServiceClient if the connection string is available.
    Returns None otherwise.
    """
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    if not connect_str:
        print("WARNING: AZURE_STORAGE_CONNECTION_STRING not found in environment variables.")
        return None
    return BlobServiceClient.from_connection_string(connect_str)

def download_blob_to_file(container_name, blob_name, file_path):
    """
    Downloads a blob to a local file.
    """
    try:
        blob_service_client = get_blob_service_client()
        if not blob_service_client:
            return False

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        
        print(f"Successfully downloaded {blob_name} from {container_name} to {file_path}")
        return True
    except Exception as e:
        print(f"Error downloading blob {blob_name}: {e}")
        return False

def upload_file_to_blob(container_name, blob_name, file_path):
    """
    Uploads a local file to a blob.
    """
    try:
        blob_service_client = get_blob_service_client()
        if not blob_service_client:
            return False

        # Create container if it doesn't exist
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            
        print(f"Successfully uploaded {file_path} to {container_name}/{blob_name}")
        return True
    except Exception as e:
        print(f"Error uploading blob {blob_name}: {e}")
        return False

def list_blobs(container_name):
    """
    Lists blobs in a container.
    """
    try:
        blob_service_client = get_blob_service_client()
        if not blob_service_client:
            return []

        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            return []
            
        blob_list = container_client.list_blobs()
        return [blob.name for blob in blob_list]
    except Exception as e:
        print(f"Error listing blobs in {container_name}: {e}")
        return []
