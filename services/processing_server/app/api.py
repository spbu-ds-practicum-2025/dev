from fastapi import FastAPI, HTTPException, Request
from app.service import ProcessingServerService

api_app = FastAPI()
service = ProcessingServerService()

# ------------------ FROM CHANGE-INFORMATION-HANDLER ------------------

@api_app.get("/image/get")
async def get_image():
    try:
        return service.return_image_json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_app.post("/image/send")
async def send_image(request: Request):
    try:
        data = await request.json()
        img_str = data.get("img_str")

        service.set_image(base64_str=img_str)
        image_data = service.return_image_json()
        if image_data is None:
            raise HTTPException(status_code=402, detail="No IMGAWGWG")
        else:
            return image_data
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error")

@api_app.post("/image/create")
async def create_new_image(request: Request):
    try:
        data = await request.json()
        height = data.get("height")
        width = data.get("width")

        service.create_new_image(height=height, width=width)
        image_data = service.return_image_json()
        if image_data is None:
            raise HTTPException(status_code=402, detail="No IMGAWGWG")
        else:
            return image_data
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error")


# ------------------ OTHER ------------------

@api_app.get("/health")
def health_check():
    return {"status": "Processing server is running"}
