class MetadataManager:
    def encrypt_metadata(self, metadata, key):
        iv, encrypted_metadata, tag = Encryptor().encrypt_data(metadata.encode(), key)
        return iv, encrypted_metadata, tag
