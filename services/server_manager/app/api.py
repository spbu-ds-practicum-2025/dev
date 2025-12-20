from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from app.service import ServerManagerService, ClientAlreadyExistsError, ClientNotFoundError, RoomAlreadyExistsError, NoFreeServerError, RedactorRoleFail

api_app = FastAPI()
service = ServerManagerService()

# ------------------ FROM API-GATEWAY ------------------

@api_app.post("/redactor_role/take/{client_id}")
def redactor_role_take(client_id: str):
    try:
        room = service.return_client_room(client_id)
        server = service.return_room_server(room)

        service.take_redactor_role(server, client_id)

        participants = service.return_room_participants(room)

        return {"participants": participants}
    except RedactorRoleFail:
        raise HTTPException(status_code=401, detail="Redactor Role Failed")

@api_app.post("/redactor_role/leave/{client_id}")
def redactor_role_leave(client_id: str):
    try:
        room = service.return_client_room(client_id)
        server = service.return_room_server(room)

        service.leave_redactor_role(server, client_id)

        participants = service.return_room_participants(room)

        return {"participants": participants}
    except RedactorRoleFail:
        raise HTTPException(status_code=401, detail="Redactor Role Failed")

@api_app.post("/client/register/{client_id}")
def register_client(client_id: str):
    try:
        service.register_client(client_id)
        return {"status": "SUCCESS"}
    except ClientAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Client already exists")

@api_app.post("/client/disconnect/{client_id}")
def disconnect_client(client_id: str):
    try:
        service.disconnect_client(client_id)
        return {"status": "Client connected successfully!"}
    except ClientNotFoundError:
        raise HTTPException(status_code=404, detail="Клиента не существует")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_app.post("/rooms/join/{room_name}/{client_id}")
def join_room(room_name: str, client_id: str):
    try:
        service.join_client_to_room(room_name, client_id)
        return {"status": "Room joined successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_app.post("/rooms/leave/{client_id}")
def leave_room(client_id: str):
    try:
        room = service.return_client_room(client_id)
        if room:
            service.remove_client_from_room(room, client_id)
        return {"status": "Room leaved successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_app.post("/rooms/create/{room_name}/{client_id}")
def create_room(room_name: str, client_id: str):
    try:
        service.create_new_room(room_name)
        service.join_client_to_room(room_name, client_id)
        return {"status": "success"}
    except RoomAlreadyExistsError:
        raise HTTPException(status_code=401, detail="Room already exists")
    except NoFreeServerError:
        raise HTTPException(status_code=402, detail="No free servers left")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_app.get("/rooms/get_info")
def get_server_data():
    server_data = service.return_server_data()
    data = {
        "type": "get_info",
        "clients": server_data["clients"],
        "rooms": server_data["rooms"]
    }
    return jsonable_encoder(data)


# ------------------ FROM CHANGE-INFORMATION-HANDLER ------------------

@api_app.get("/server/port/get/{client_id}")
def return_server_port_by_client(client_id: str):
    try:
        port = service.return_processing_server_port_by_client_id(client_id)
        if port is None:
            raise HTTPException(status_code=404, detail="No server behind client aaaaaaaaaaaaaaa why")
        return {"port": port}
    except Exception:
        raise HTTPException(status_code=400, detail="Client already exists")

@api_app.get("/rooms/participants/get/{client_id}")
def return_room_participants_by_client(client_id: str):
    try:
        room = service.return_client_room(client_id)
        participants = service.return_room_participants(room)

        if participants is None:
            raise HTTPException(status_code=404, detail="No participants in room")
        return {"participants": participants}
    except Exception:
        raise HTTPException(status_code=400, detail="Client already exists")


# ------------------ OTHER ------------------

@api_app.get("/health")
def health_check():
    return {"status": "Server Manager is running"}
