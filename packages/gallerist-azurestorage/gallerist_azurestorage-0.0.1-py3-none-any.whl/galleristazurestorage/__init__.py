from gallerist.abc import SyncFileStore
from azure.storage.common import CloudStorageAccount


class AzureBlobFileStore(SyncFileStore):

    def __init__(self, account: CloudStorageAccount, container_name: str):
        self.account = account
        self.service = account.create_block_blob_service()
        self.container_name = container_name

    @classmethod
    def from_name_and_key(cls,
                          account_name: str,
                          account_key: str,
                          container_name: str):
        return cls(CloudStorageAccount(account_name=account_name, account_key=account_key), container_name)

    def read_file(self, file_path: str) -> bytes:
        blob = self.service.get_blob_to_bytes(self.container_name, file_path)
        return blob.content

    def write_file(self, file_path: str, data: bytes):
        self.service.create_blob_from_bytes(self.container_name, file_path, data)

    def delete_file(self, file_path: str):
        self.service.delete_blob(self.container_name, file_path)

