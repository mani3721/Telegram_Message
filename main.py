from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.services.session_manager import get_client
from src.services.send_message import send_to_chat
from src.services.get_chats import get_chat_list
import asyncio

app = FastAPI()

class LoginBody(BaseModel):
    phone: str
    otp: str | None = None
    phone_code_hash: str | None = None
    twofa: str | None = None


@app.post("/auth/login")
async def full_login(data: LoginBody):
    client = get_client()
    await client.connect()

    try:
        # 1. First-time login (no OTP yet)
        if not await client.is_user_authorized() and not data.otp:
            sent = await client.send_code_request(data.phone)
            return {
                "status": "code_sent",
                "phone_code_hash": sent.phone_code_hash
            }

        # 2. Submit OTP
        elif data.otp:
            try:
                await client.sign_in(data.phone, data.otp, phone_code_hash=data.phone_code_hash)
                return {"status": "logged_in"}
            except Exception as e:
                # 3. If 2FA required
                if "SESSION_PASSWORD_NEEDED" in str(e).upper():
                    if data.twofa:
                        await client.sign_in(password=data.twofa)
                        return {"status": "logged_in_with_2fa"}
                    return {"status": "2fa_required", "message": "Please enter 2FA password"}
                raise HTTPException(status_code=401, detail=str(e))
        else:
            return {"status": "invalid_input"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Existing APIs
@app.get("/chats")
async def get_chats():
    return await get_chat_list()

@app.post("/send")
async def send(chat_id: int, message: str):
    await send_to_chat(chat_id, message)
    return {"status": "sent", "chat_id": chat_id}
