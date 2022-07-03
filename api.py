import uvicorn
from fastapi import FastAPI
from pydantic import BaseSettings

class EmailSchema(BaseModel):
   email: List[EmailStr]


conf = ConnectionConfig(
   MAIL_USERNAME=from_,
   MAIL_PASSWORD="************",
   MAIL_PORT=587,
   MAIL_SERVER="smtp.gmail.com",
   MAIL_TLS=True,
   MAIL_SSL=False
)

message = MessageSchema(
       subject="Fastapi-Mail module",
       recipients=email.dict().get("email"),
       body=template,
       subtype="html"
       )
settings = Settings()
app = FastAPI()


@app.post("/send_mail")
async def send_mail(email: EmailSchema):

	template = """
		<html>
		<body>


<p>Hi !!!
		<br>Kaza Tespit Sistemi</p>


		</body>
		</html>
		"""

	message = MessageSchema(
		subject="Fastapi-Mail module",
		recipients=email.dict().get("email"),
		body=template,
		subtype="html"
		)

	fm = FastMail(conf)
	await fm.send_message(message)
		print(message)



	return JSONResponse(status_code=200, content={"message": "email has been sent"})


@app.get("/settings")
def get_settings():
    return { "message": settings.message }

if __name__ == "__main__":
    uvicorn.run("api:app")
