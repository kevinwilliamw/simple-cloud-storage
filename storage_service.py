import dependencies

from nameko.rpc import rpc

class StorageService:

    name = 'storage_service'

    database = dependencies.Database()

    @rpc
    def add_user(self, username, password):
        user = self.database.add_user(username, password)
        return user

    @rpc
    def get_user(self, username, password):
        user = self.database.get_user(username, password)
        return user
    
    @rpc
    def upload_file(self, content, owner):
        user = self.database.upload_file(content, owner)
        return user
    
    @rpc
    def download_file(self, uuid, currentUser):
        user = self.database.download_file(uuid, currentUser)
        return user