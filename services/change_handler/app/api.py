import requests
from fastapi import FastAPI, HTTPException, Request

api_app = FastAPI()

SERVER_MANAGER_URL = "http://server_manager:8081"


# ------------------ FROM API-GATEWAY ------------------

@api_app.get("/image/get/{client_id}")
async def get_image(client_id: str):
    try:

        response1 = requests.get(f"{SERVER_MANAGER_URL}/server/port/get/{client_id}")
        data1 = response1.json()
        port = data1.get("port")

        if not port:
            raise HTTPException(status_code=400, detail="No port")

        # Получение изображения с сервера
        PROCESSING_SERVER_URL = f"http://processing_server_{str(port)[-1]}:{port}"
        response2 = requests.get(f"{PROCESSING_SERVER_URL}/image/get")
        response3 = requests.get(f"{SERVER_MANAGER_URL}/rooms/participants/get/{client_id}")

        # Отправка изображения с сервера
        data2 = response2.json()
        data3 = response3.json()

        if data2 is not None:
            image_data = data2.get("data")
        else:
            image_data = None

        participants = data3.get("participants")
        return {"data": image_data, "participants": participants}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=402, detail="Error")

@api_app.post("/image/send/{client_id}")
async def send_image(request: Request, client_id: str):
    try:
        data = await request.json()
        img_str = data.get("img_str")

        # Получение сервера, на котором находится клиент
        response1 = requests.get(f"{SERVER_MANAGER_URL}/server/port/get/{client_id}")
        data1 = response1.json()
        port = data1.get("port")

        if not port:
            raise HTTPException(status_code=400, detail="No port")

        # Обновление изображения на сервере
        PROCESSING_SERVER_URL = f"http://processing_server_{str(port)[-1]}:{port}"
        response2 = requests.post(
            f"{PROCESSING_SERVER_URL}/image/send",
            json={
                "img_str": img_str
            }
        )

        # Получение списка участников сервера
        response3 = requests.get(f"{SERVER_MANAGER_URL}/rooms/participants/get/{client_id}")

        # Отправка изображения с сервера
        data2 = response2.json()
        data3 = response3.json()
        image_data = data2.get("data")
        participants = data3.get("participants")

        return {"data": image_data, "participants": participants}

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=402, detail="Error")

@api_app.post("/image/create/{client_id}")
async def create_new_image(request: Request, client_id: str):
    try:
        # Получение размеров из Request
        data = await request.json()
        height = data.get("height")
        width = data.get("width")

        # Получение сервера, на котором находится клиент
        response1 = requests.get(f"{SERVER_MANAGER_URL}/server/port/get/{client_id}")
        data1 = response1.json()
        port = data1.get("port")

        if not port:
            raise HTTPException(status_code=400, detail="No port")

        # Создание нового изображения на сервере
        PROCESSING_SERVER_URL = f"http://processing_server_{str(port)[-1]}:{port}"
        response2 = requests.post(
            f"{PROCESSING_SERVER_URL}/image/create",
            json={
                "height": height,
                "width": width
            }
        )

        # Получение списка участников сервера
        response3 = requests.get(f"{SERVER_MANAGER_URL}/rooms/participants/get/{client_id}")

        # Отправка изображения с сервера
        data2 = response2.json()
        data3 = response3.json()
        image_data = data2.get("data")
        participants = data3.get("participants")

        return {"data": image_data, "participants": participants}

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=402, detail="Error")

# ------------------ OTHER ------------------

@api_app.get("/health")
def health_check():
    return {"status": "Change Information Handler is running"}
