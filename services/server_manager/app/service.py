import docker

class ServerManagerService:
    def __init__(self):
        self.clients = {}
        self.rooms = {}
        self.servers = {}

        self.servers_count = 0
        self.get_processing_servers_list()

    def get_processing_servers_list(self):
        client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
        containers = client.containers.list()

        processing_servers = [container for container in containers if "processing_server" in container.name]
        self.servers_count = len(processing_servers)
        for server in processing_servers:
            port = list(server.attrs['NetworkSettings']['Ports'].keys())[0][:4]
            self.servers[server.name] = {"port": port, "room": None, "redactor": None}

        print(self.servers)

    def is_client_exists(self, client_id):
        return client_id in self.clients.keys()

    def register_client(self, client_id):
        if self.is_client_exists(client_id):
            raise ClientAlreadyExistsError

        self.clients[client_id] = {}
        return client_id

    def return_client_room(self, client_id):
        if not self.is_client_exists(client_id):
            raise ClientNotFoundError
        for room in self.rooms.keys():
            if self.is_client_in_room(room, client_id):
                return room
        return None

    def remove_client_from_room(self, room_name, client_id):
        if not self.is_room_exist(room_name):
            raise RoomNotFoundError
        if not self.is_client_exists(client_id):
            raise ClientNotFoundError
        if not self.is_client_in_room(room_name, client_id):
            raise ClientNotFoundInRoomError

        self.take_all_redactor_rights(client_id)
        self.rooms[room_name].remove(client_id)

    def remove_client_from_all_rooms(self, client_id):
        if not self.is_client_exists(client_id):
            raise ClientNotFoundError
        for room in self.rooms.keys():
            if self.is_client_in_room(room, client_id):
                self.rooms[room].remove(client_id)

    def take_all_redactor_rights(self, client_id):
        if not self.is_client_exists(client_id):
            raise ClientNotFoundError
        for server in self.servers.keys():
            if self.servers[server]["redactor"] == client_id:
                self.servers[server]["redactor"] = None

    def disconnect_client(self, client_id):
        if not self.is_client_exists(client_id):
            raise ClientNotFoundError
        self.remove_client_from_all_rooms(client_id)
        self.take_all_redactor_rights(client_id)
        self.clients.pop(client_id)

    def return_clients_list(self):
        return list(self.clients.keys())

    def is_room_exist(self, room_name):
        return room_name in self.rooms.keys()

    def create_new_room(self, room_name):
        if self.is_room_exist(room_name):
            raise RoomAlreadyExistsError
        if self.is_any_server_free():
            server = self.return_first_free_server()
            self.rooms[room_name] = []
            self.servers[server]["room"] = room_name
            # print("Создание новой комнаты:", server, room_name, self.servers[server]["room"])
        else:
            raise NoFreeServerError

    def join_client_to_room(self, room_name, client_id):
        if not self.is_room_exist(room_name):
            raise RoomNotFoundError
        if not self.is_client_exists(client_id):
            raise ClientNotFoundError
        for room in self.rooms.keys():
            if self.is_client_in_room(room, client_id):
                self.remove_client_from_room(room, client_id)
        self.rooms[room_name].append(client_id)

    def is_client_in_room(self, room_name, client_id):
        if not self.is_room_exist(room_name):
            raise RoomNotFoundError
        if not self.is_client_exists(client_id):
            raise ClientNotFoundError
        return client_id in self.rooms[room_name]

    def return_server_data(self):
        return {
            "clients": list(self.clients.keys()),
            "rooms": self.rooms
        }

    def is_any_server_free(self):
        for server in self.servers.keys():
            if self.servers[server]["room"] is None:
                return True
        return False

    def return_first_free_server(self):
        for server in self.servers.keys():
            if self.servers[server]["room"] is None:
                return server
        return None

    def return_room_server(self, room_name):
        if not self.is_room_exist(room_name):
            raise RoomNotFoundError
        for server in self.servers.keys():
            if self.servers[server]["room"] == room_name:
                return server
        return None

    def return_processing_server_port_by_client_id(self, client_id):
        if not self.is_client_exists(client_id):
            raise ClientNotFoundError

        room = self.return_client_room(client_id)
        if not room:
            raise RoomNotFoundError

        server = self.return_room_server(room)

        return self.servers[server]["port"]

    def return_room_participants(self, room_name):
        if not self.is_room_exist(room_name):
            raise RoomNotFoundError
        return self.rooms[room_name]

    def is_server_redactor_role_free(self, server) -> bool:
        return self.servers[server]["redactor"] is None

    def take_redactor_role(self, server, client_id):
        if not self.is_client_exists(client_id):
            raise ClientNotFoundError
        if self.servers[server]["redactor"] is None:
            self.servers[server]["redactor"] = client_id
        else:
            raise RedactorRoleFail

    def leave_redactor_role(self, server, client_id):
        if not self.is_client_exists(client_id):
            raise ClientNotFoundError
        if self.servers[server]["redactor"] == client_id:
            self.servers[server]["redactor"] = None
        else:
            raise RedactorRoleFail


class ClientAlreadyExistsError(Exception):
    pass

class ClientNotFoundError(Exception):
    pass

class ClientNotFoundInRoomError(Exception):
    pass

class RoomAlreadyExistsError(Exception):
    pass

class RoomNotFoundError(Exception):
    pass

class NoFreeServerError(Exception):
    pass

class RedactorRoleFail(Exception):
    pass
