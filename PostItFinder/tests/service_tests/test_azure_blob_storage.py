from django.conf import settings
from PostItFinder import create_and_store_pptx
import unittest
import os
from io import BytesIO
from datetime import datetime
import uuid

from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient

# ================================================================================================
# HELPER FUNCTIONS
# ================================================================================================
def get_file_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.abspath(os.path.join(current_dir, os.pardir))
    return os.path.join(test_path, "resources", "test_images", file_name)

def get_container_name():
    now = datetime.now()
    return f"test-{now.strftime('%Y%m%d%H%M%S%f')}-{uuid.uuid4()}"

def delete_test_containers():
    # delete all test containers
    try:
        blob_service_client = BlobServiceClient.from_connection_string(os.getenv('SNIP_BLOB_STORAGE_CONN_STR'))
    except Exception as err:
        print(f"Another exception occurred: {err}")
        return False
    
    # get all containers whose name starts with "test-", and delete
    test_containers = blob_service_client.list_containers(name_starts_with='test-',
                                                        include_metadata=True)
    test_container_names = [c["name"] for c in test_containers]

    # delete all test containers
    for name in test_container_names:
        blob_service_client.delete_container(name)

    return True


# ================================================================================================
# TEST CLASSES
# ================================================================================================
class TestCreateBlobServiceClient(unittest.TestCase):
    def setUp(self):       
        self.conn_str = os.getenv('SNIP_BLOB_STORAGE_CONN_STR')
        self.container_name = get_container_name()

    def tearDown(self):
        del(self.conn_str, self.container_name)
    
    def test_valid_connect_str_returns_blobserviceclient_obj(self):        
        sftabs = create_and_store_pptx.SaveFileToAzureBlobStorage(connect_str=self.conn_str,
                                                                container_name=self.container_name)

        result = sftabs.create_blob_service_client()
        self.assertIsInstance(result, BlobServiceClient)                     

    def test_invalid_connect_str_returns_none(self):
        sftabs = create_and_store_pptx.SaveFileToAzureBlobStorage(connect_str="invalid conn str",
                                                                container_name=self.container_name)

        result = sftabs.create_blob_service_client()
        self.assertIsNone(result)

    def test_connect_str_is_empty_returns_none(self):
        sftabs = create_and_store_pptx.SaveFileToAzureBlobStorage(connect_str="",
                                                                container_name=self.container_name)

        result = sftabs.create_blob_service_client()
        self.assertIsNone(result)
    
    def test_connect_str_is_none_returns_none(self):
        """
        Check that if the connection string used is None, then None is returned.

        NOTE: this case activates the AttributeError exception
        """
        sftabs = create_and_store_pptx.SaveFileToAzureBlobStorage(connect_str=None,
                                                                container_name=self.container_name)

        result = sftabs.create_blob_service_client()
        self.assertIsNone(result)
    
# ------------------------------------

class TestCreateContainer(unittest.TestCase):
    def setUp(self):       
        self.conn_str = os.getenv('SNIP_BLOB_STORAGE_CONN_STR')

    def tearDown(self):
        delete_tc = delete_test_containers()
        if not delete_tc:
            print(f"*** ERROR: The BlobServiceClient was not created successfully. ***")
        del(self.conn_str)

    def test_unique_container_name_works_correctly(self):
        """
        Check that when we attempt to create a container with a unique name:
        - The container is indeed created;
        - create_container() returns a ContainerClient object;
        - The object allows public access to blobs only.
        """
        # generate a unique container name
        container_name = get_container_name()

        # create a new (temporary) container
        sftabs = create_and_store_pptx.SaveFileToAzureBlobStorage(connect_str=self.conn_str,
                                                                container_name=container_name)
        container = sftabs.create_container()
        # check that 'container' is a ContainerClient object
        self.assertIsInstance(container, ContainerClient)

        # create a BlobServiceClient for next checks
        try:
            blob_service_client = BlobServiceClient.from_connection_string(self.conn_str)
        except Exception as err:
            self.fail(f"The BlobServiceClient was not created successfully. Sys error: {err}")
        
        # get all containers whose name starts with "test-", and check our container is there
        test_containers = blob_service_client.list_containers(name_starts_with='test-',
                                                            include_metadata=True)
        test_container_names = [c["name"] for c in test_containers]
        self.assertIn(container_name, test_container_names)

        # check that the container has public access permissions for 'blob' only
        # (i.e. not for the container itself)
        props = container.get_container_properties()
        self.assertEqual(props["public_access"], "blob")

    def test_non_unique_container_name_returns_none(self):
        """
        Check that when we attempt to create a container with a name that already 
        exists in the same blob storage account, None is returned
        """
        # generate a unique container name        
        container_name = get_container_name()

        # create a new (temporary) container
        sftabs = create_and_store_pptx.SaveFileToAzureBlobStorage(connect_str=self.conn_str,
                                                                container_name=container_name)
        container = sftabs.create_container()
        # check that 'container' is a ContainerClient object
        self.assertIsInstance(container, ContainerClient)
        
        # create another container with the same name
        sftabs2 = create_and_store_pptx.SaveFileToAzureBlobStorage(connect_str=self.conn_str,
                                                                container_name=container_name)
        container2 = sftabs2.create_container()
        # check that container2 is None
        self.assertIsNone(container2)

    def test_invalid_connection_str_returns_none(self):
        """
        Check that using an invalid connection string to create the container returns
        None.
        """
        # generate a unique container name        
        container_name = get_container_name()

        # create a new (temporary) container
        sftabs = create_and_store_pptx.SaveFileToAzureBlobStorage(connect_str="invalid-conn-str",
                                                                container_name=container_name)
        container = sftabs.create_container()
        # check that 'container' is None
        self.assertIsNone(container)
    
    def test_invalid_container_name_returns_none(self):
        """
        Container naming in Azure Blob Storage is quite constrained; only alphanumeric
        chars and '-' are allowed, and only lower-case alpha (full rules:
        https://docs.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#container-names)

        Check that if an invalid name is provided, None is returned.
        """
        # generate an invalid container name
        container_name = "invalid_container_name"

        # create a new (temporary) container
        sftabs = create_and_store_pptx.SaveFileToAzureBlobStorage(connect_str=self.conn_str,
                                                                container_name=container_name)
        container = sftabs.create_container()
        # check that 'container' is None
        self.assertIsNone(container)

# ------------------------------------

class TestCreateBlobClient(unittest.TestCase):
    def setUp(self):       
        self.conn_str = os.getenv('SNIP_BLOB_STORAGE_CONN_STR')

    def tearDown(self):
        delete_tc = delete_test_containers()
        if not delete_tc:
            print(f"*** ERROR: The BlobServiceClient was not created successfully. ***")
        del(self.conn_str)

    def test_correct_input_successfully_creates_blob_client(self):
        # generate a unique container name        
        container_name = get_container_name()

        # create a new object and container
        sftabs = create_and_store_pptx.SaveFileToAzureBlobStorage(connect_str=self.conn_str,
                                                                container_name=container_name)        
        # container = sftabs.create_container()
        sftabs.create_container()

        # create a blob client object and check that it is a valid BlobClient 
        # object
        blob_client = sftabs.create_blob_client("test.txt")
        self.assertIsInstance(blob_client, BlobClient)

    def test_invalid_connect_str_returns_none(self):
        # generate a unique container name
        container_name = get_container_name()

        # create a new object with invalid connection string
        sftabs = create_and_store_pptx.SaveFileToAzureBlobStorage(connect_str="invalid-conn-str",
                                                                container_name=container_name)
        
        # create a blob client object
        blob_client = sftabs.create_blob_client("test.txt")
        self.assertIsNone(blob_client)

    def test_nonexistent_container_and_blob_does_not_raise_error(self):
        """
        This is more of a gotcha than desired behaviour, and is mainly to confirm
        that what I think happens, actually *does* happen (i.e. that trying to 
        create a blob client using a container name for a container that doesn't 
        exist, and a file that doesn't exist, doesn't raise an exception).
        """
        # generate a unique container name        
        container_name = get_container_name()

        # create a new object, but *DO NOT* create a new container
        sftabs = create_and_store_pptx.SaveFileToAzureBlobStorage(connect_str=self.conn_str,
                                                                container_name=container_name)
        
        # create a blob client object and check that it is a valid BlobClient 
        # object, even though the container and file don't exist
        # [NOTE: there's no fixtures file called 'test.txt']
        blob_client = sftabs.create_blob_client("test.txt")
        self.assertIsInstance(blob_client, BlobClient)        

# ------------------------------------

class TestUploadBytesToContainer(unittest.TestCase):
    def setUp(self):       
        self.conn_str = os.getenv('SNIP_BLOB_STORAGE_CONN_STR')
        # generate a unique container name        
        self.container_name = get_container_name()

        # set the test file to be a very small (1KB) file
        self.file = "test_file.txt"
        self.file_path = get_file_path(self.file)

    def tearDown(self):
        delete_tc = delete_test_containers()
        if not delete_tc:
            print(f"*** ERROR: The BlobServiceClient was not created successfully. ***")
        del(self.conn_str, self.container_name)

    def test_correct_input_successfully_uploads_blob(self):
        """
        NOTE: the test below relies on  a *reasonably* good Internet connection to
        upload the test image. If the connection isn't good enough, the connection
        will time out, the test will fail and None will be returned.
        """
        sftabs = create_and_store_pptx.SaveFileToAzureBlobStorage(connect_str=self.conn_str,
                                                                container_name= self.container_name)
        
        # create the container
        container = sftabs.create_container()

        # read the binary contents of the test file, and convert to file-like object 
        # using BytesIO
        with open(self.file_path, "rb") as f:
            img_bytes = f.read()         
        bytes_out = BytesIO(img_bytes)

        # try to upload the file
        if container is not None:                          
            url = sftabs.upload_bytes_to_container(self.file, bytes_out.getvalue())
        else:
            self.fail("The container was not created correctly.")

        self.assertIsNotNone(url)

        # check that the file appears in the container
        blobs_in_container = [blob.name for blob in container.list_blobs()]
        self.assertIn(self.file, blobs_in_container)

    def test_invalid_file_returns_none(self):
        sftabs = create_and_store_pptx.SaveFileToAzureBlobStorage(connect_str=self.conn_str,
                                                                container_name= self.container_name)
        
        # create the container
        container = sftabs.create_container()

        # read the binary contents of the test file, and convert to file-like object 
        # using BytesIO
        with open(self.file_path, "rb") as f:
            img_bytes = f.read()         
        bytes_out = BytesIO(img_bytes)

        # try to upload the file, slicing the last byte off the end to invalidate it
        if container is not None:                          
            url = sftabs.upload_bytes_to_container(self.file, bytes_out.getvalue()[-1])
        else:
            self.fail("The container was not created correctly.")

        self.assertIsNone(url)

        # check that the file does not appear in the container
        blobs_in_container = [blob.name for blob in container.list_blobs()]
        self.assertNotIn(self.file, blobs_in_container)

    def test_filename_set_correctly(self):
        """
        Ensure that the filename provided is used for the blob
        """
        sftabs = create_and_store_pptx.SaveFileToAzureBlobStorage(connect_str=self.conn_str,
                                                                container_name= self.container_name)
        
        # create the container
        container = sftabs.create_container()

        # read the binary contents of the test file, and convert to file-like object 
        # using BytesIO
        with open(self.file_path, "rb") as f:
            img_bytes = f.read()         
        bytes_out = BytesIO(img_bytes)

        tmp_filename = "fake_file"

        # try to upload the file
        if container is not None:                          
            # url = sftabs.upload_bytes_to_container(tmp_filename, bytes_out.getvalue())
            sftabs.upload_bytes_to_container(tmp_filename, bytes_out.getvalue())
        else:
            self.fail("The container was not created correctly.")
        
        # check that the file appears in the container
        blobs_in_container = [blob.name for blob in container.list_blobs()]
        self.assertIn(tmp_filename, blobs_in_container)

# ------------------------------------

# class TestCreateContainerAndUploadFile(unittest.TestCase):
#     def setUp(self):       
#         self.conn_str = os.getenv('SNIP_BLOB_STORAGE_CONN_STR')
#         # generate a unique container name        
#         self.container_name = get_container_name()

#         # set the test file to be a very small (1KB) file
#         self.file = "test_file.txt"
#         self.file_path = get_file_path(self.file)

#     def tearDown(self):
#         delete_tc = delete_test_containers()
#         if not delete_tc:
#             print(f"*** ERROR: The BlobServiceClient was not created successfully. Sys error: {err} ***")
#         del(self.conn_str, self.container_name)