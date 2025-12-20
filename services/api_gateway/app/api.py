import json
import uuid
import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException
from websockets import ConnectionClosed

SERVER_MANAGER_URL = "http://server_manager:8081"
CHANGE_INFORMATION_HANDLER_URL = "http://change_handler:8082"

api_app = FastAPI()
connected_clients: dict[str, WebSocket] = {}

@api_app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_id = str(uuid.uuid4())

    connected_clients[client_id] = websocket
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVER_MANAGER_URL}/client/register/{client_id}")
        if response.status_code != 200:
            await websocket.send_text(json.dumps(response.json()))
            await websocket.close()
            return

    try:
        while True:
            data = json.loads(await websocket.receive_text())
            msg_type = data.get("type")

            # --------------------- ROOMS-MENU ---------------------

            if msg_type == "create_room":
                room_name = data.get("room_name")
                print(f"Получен запрос на создание комнаты {room_name}!")
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{SERVER_MANAGER_URL}/rooms/create/{room_name}/{client_id}")
                    if response.status_code == 200:
                        print(f"Запрос на создание комнаты {room_name}: УСПЕХ!")
                        await websocket.send_text(json.dumps({"type": "create_room", "status": "success"}))
                    elif response.status_code == 401:
                        print(f"Запрос на создание комнаты {room_name}: ОШИБКА, уже существует!")
                        await websocket.send_text(json.dumps({"type": "create_room", "status": "fail", "detail": "already_exists"}))
                    elif response.status_code == 402:
                        print(f"Запрос на создание комнаты {room_name}: ОШИБКА, нет свободных серверов!")
                        await websocket.send_text(json.dumps({"type": "create_room", "status": "fail", "detail": "no_server"}))
                    else:
                        print(f"Запрос на создание комнаты {room_name}: ОШИБКА!")
                        await websocket.send_text(json.dumps({"type": "create_room", "status": "fail", "detail": "Unknown"}))

            elif msg_type == "join_room":
                room_name = data.get("room_name")
                print(f"Получен запрос на присоединение к комнате {room_name}!")
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{SERVER_MANAGER_URL}/rooms/join/{room_name}/{client_id}")
                    if response.status_code == 200:
                        print(f"Запрос на подключение к комнате {room_name}: УСПЕХ!")
                        await websocket.send_text(json.dumps({"type": "join_room", "status": "success"}))
                    else:
                        print(f"Запрос на подключение к комнате {room_name}: ПРОВАЛ!")
                        await websocket.send_text(json.dumps({"type": "join_room", "status": "fail"}))

            elif msg_type == "get_info":
                print("Получен запрос на обновление данных!")
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{SERVER_MANAGER_URL}/rooms/get_info")
                    if response.status_code == 200:
                        print("Получен запрос на обновление данных: УСПЕХ!")
                        await websocket.send_text(json.dumps({"type": "get_info", "status": "success", "data": response.json()}))
                    else:
                        print("Получен запрос на обновление данных: ОШИБКА!")
                        await websocket.send_text(json.dumps({"type": "get_info", "status": "fail", "data": response.json()}))

            # --------------------- MULTI-EDITOR ---------------------

            elif msg_type == "leave_room":
                print("Получен запрос на выход из комнаты!")
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{SERVER_MANAGER_URL}/rooms/leave/{client_id}")
                    if response.status_code == 200:
                        print(f"Запрос на выход из комнаты: УСПЕХ!")
                        await websocket.send_text(json.dumps({"type": "leave_room", "status": "success"}))
                    else:
                        print(f"Запрос на выход из комнаты: ОШИБКА!")
                        await websocket.send_text(json.dumps({"type": "leave_room", "status": "fail"}))

            elif msg_type == "get_image":
                print("Получен запрос на загрузку изображения с сервера!")
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{CHANGE_INFORMATION_HANDLER_URL}/image/get/{client_id}")
                    if response.status_code == 200:
                        print(f"Запрос на загрузку изображения: УСПЕХ!")
                        data = response.json()
                        image_data = data.get("data")
                        participants = data.get("participants")
                        print(participants, image_data)

                        if participants is not None:
                            for client_id in connected_clients.keys():
                                if client_id in participants:
                                    client_socket = connected_clients[client_id]
                                    await client_socket.send_text(
                                        json.dumps({
                                                "type": "get_image",
                                                "status": "success",
                                                "data": image_data
                                            }
                                        )
                                    )

            elif msg_type == "send_image":
                print("Получен запрос на отправку изображения на сервер!")
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{CHANGE_INFORMATION_HANDLER_URL}/image/send/{client_id}", json={"img_str": data["img_str"]})
                    if response.status_code == 200:
                        print(f"Запрос на отправку изображения: УСПЕХ!")
                        data = response.json()
                        image_data = data.get("data")
                        participants = data.get("participants")
                        print(participants, image_data)

                        if participants is not None:
                            for client_id in connected_clients.keys():
                                if client_id in participants:
                                    client_socket = connected_clients[client_id]
                                    await client_socket.send_text(
                                        json.dumps({
                                                "type": "get_image",
                                                "status": "success",
                                                "data": image_data
                                            }
                                        )
                                    )

            elif msg_type == "create_new_image":
                print("Получен запрос на создание нового изображения!")
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{CHANGE_INFORMATION_HANDLER_URL}/image/create/{client_id}", json={'width': data["width"], 'height': data["height"]})
                    if response.status_code == 200:
                        print(f"Запрос на создание изображения: УСПЕХ!")
                        data = response.json()
                        image_data = data.get("data")
                        participants = data.get("participants")
                        print(participants, image_data)

                        if participants is not None:
                            for client_id in connected_clients.keys():
                                if client_id in participants:
                                    client_socket = connected_clients[client_id]
                                    await client_socket.send_text(
                                        json.dumps(
                                            {
                                                "type": "create_new_image",
                                                "status": "success",
                                                "data": image_data
                                            }
                                        )
                                    )
                    else:
                        print(f"Запрос на создание изображения: ОШИБКА!")
                        await websocket.send_text(json.dumps({"type": "create_new_image", "status": "fail"}))

            elif msg_type == "take_redactor_role":
                print("Получен запрос на получение роли редактора!")
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{SERVER_MANAGER_URL}/redactor_role/take/{client_id}")
                    if response.status_code == 200:
                        print(f"Запрос на получение роли редактора: УСПЕХ!")

                        data = response.json()
                        participants = data.get("participants")

                        await websocket.send_text(json.dumps({"type": "take_redactor_role", "status": "success", "detail": "redactor"}))
                        if participants is not None:
                            for other_client_id in connected_clients.keys():
                                if other_client_id != client_id and other_client_id in participants:
                                    client_socket = connected_clients[other_client_id]
                                    await client_socket.send_text(
                                        json.dumps(
                                            {
                                                "type": "take_redactor_role",
                                                "status": "success",
                                                "detail": "not_redactor"
                                            }
                                        )
                                    )
                    elif response.status_code == 401:
                        await websocket.send_text(json.dumps({"type": "take_redactor_role", "status": "fail", "detail": "Роль редактора уже занята!"}))
                        print(f"Запрос на занатие роли редактора: ОШИБКА!")

            elif msg_type == "leave_redactor_role":
                print("Получен запрос снятие роли редактора!")
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{SERVER_MANAGER_URL}/redactor_role/leave/{client_id}")
                    if response.status_code == 200:
                        print(f"Запрос на снятие роли редактора: УСПЕХ!")

                        data = response.json()
                        participants = data.get("participants")

                        if participants is not None:
                            for client_id in connected_clients.keys():
                                if client_id in participants:
                                    client_socket = connected_clients[client_id]
                                    await client_socket.send_text(
                                        json.dumps(
                                            {
                                                "type": "leave_redactor_role",
                                                "status": "success",
                                            }
                                        )
                                    )
                    elif response.status_code == 401:
                        await websocket.send_text(json.dumps({"type": "leave_redactor_role", "status": "fail", "detail": "Роль редактора не занята!"}))
                        print(f"Запрос на снятие роли редактора: ОШИБКА!")

            # --------------------- OTHER ---------------------

            else:
                print(f"НЕИЗВЕСТНЫЙ ЗАПРОС: {msg_type}")

    except WebSocketDisconnect:
        print(f"Отключён: {client_id}")

    finally:
        print(f"Закрываем соединение с клиентов {client_id}")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{SERVER_MANAGER_URL}/client/disconnect/{client_id}")
                connected_clients.pop(client_id, None)
        except Exception:
            await client.post(f"{SERVER_MANAGER_URL}/client/disconnect/{client_id}")



