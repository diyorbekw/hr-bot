import asyncio
from fastapi import FastAPI
from main import dp, bot, main  # main.py dan import qilamiz

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # Botni alohida task qilib fon rejimida ishga tushuramiz
    asyncio.create_task(dp.start_polling(bot))
    print("Bot va FastAPI ishga tushdi.")

@app.get("/")
async def root():
    return {"message": "Bot ishlayapti ✅"}
