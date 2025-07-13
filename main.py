from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.services.session_manager import get_client
from src.services.send_message import send_to_chat
from src.services.get_chats import get_chat_list
import asyncio

app = FastAPI()

# Models for auth flow
class LoginRequest(BaseModel):
    phone: str

class ConfirmCode(BaseModel):
    phone: str
    code: str
    phone_code_hash: str

class TwoFARequest(BaseModel):
    password: str

# Step 1: Send code to phone
@app.post("/auth/start-login")
async def start_login(req: LoginRequest):
    client = get_client()
    await client.connect()
    if not await client.is_user_authorized():
        try:
            sent = await client.send_code_request(req.phone)
            return {"status": "code_sent", "phone_code_hash": sent.phone_code_hash}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"status": "already_logged_in"}

# Step 2: Confirm login with OTP and hash
@app.post("/auth/confirm-code")
async def confirm_code(data: ConfirmCode):
    client = get_client()
    await client.connect()
    try:
        await client.sign_in(
            phone=data.phone,
            code=data.code,
            phone_code_hash=data.phone_code_hash
        )
        return {"status": "logged_in"}
    except Exception as e:
        # If 2FA required, you'll get SessionPasswordNeededError
        if "SESSION_PASSWORD_NEEDED" in str(e).upper():
            return {"status": "2fa_required"}
        raise HTTPException(status_code=401, detail=str(e))

# Step 3: Submit 2FA password if required
@app.post("/auth/2fa")
async def confirm_2fa(data: TwoFARequest):
    client = get_client()
    await client.connect()
    try:
        await client.sign_in(password=data.password)
        return {"status": "logged_in_with_2fa"}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

# Existing APIs
@app.get("/chats")
async def get_chats():
    return await get_chat_list()

@app.post("/send")
async def send(chat_id: int, message: str):
    await send_to_chat(chat_id, message)
    return {"status": "sent", "chat_id": chat_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)