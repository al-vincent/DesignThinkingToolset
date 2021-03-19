import os
from azure.storage.blob import BlobServiceClient

def delete_containers(name_prefix):
    # delete all test containers
    try:
        blob_service_client = BlobServiceClient.from_connection_string(os.getenv('SNIP_BLOB_STORAGE_CONN_STR'))
    except Exception as err:
        print(f"Another exception occurred: {err}")
        return False
    
    # get all containers whose name starts with "test-", and delete
    test_containers = blob_service_client.list_containers(name_starts_with=name_prefix,
                                                        include_metadata=True)
    test_container_names = [c["name"] for c in test_containers]

    # delete all test containers
    for name in test_container_names:
        try: 
            blob_service_client.delete_container(name)
            print(f"Deleted container {name}")
        except Exception as err:
            print(f"*** ERROR: Failed to delete container {name}. Err={err} ***")

    return True

def main():
    name_patterns_to_delete = "202101"
    delete_containers(name_patterns_to_delete)

if __name__ == "__main__":
    main()