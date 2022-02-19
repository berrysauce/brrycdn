# IMPORTS ###############################################
import logging
import os
import uvicorn
from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from tools import hashing
import random
import string


# SETUP #################################################

# Initialize logger
logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s - [%(levelname)s] @ %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S'
)

# Load enviromental variables
load_dotenv()
APP_PASSWORD = os.getenv("PASSWORD")
APP_ID_LEN = int(os.getenv("ID_LEN"))
APP_DOMAIN = os.getenv("DOMAIN")

# Initializing FastAPI
app = FastAPI()

# Mounting and selecting assets/templates directories
app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")
templates = Jinja2Templates(directory="templates")


# MAIN FUNCTIONS ########################################

@app.get("/", response_class=HTMLResponse)
def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
def post_upload(request: Request, password: str = Form(...), file: UploadFile = File(...)):
    if hashing.verifypw(APP_PASSWORD, password) is False:
        logging.warning("Unauthorized upload - wrong password")
        raise HTTPException(status_code=401, detail="Unauthorized")

    allowed_types = ["image", "video", "audio", "text"]
    if file.content_type.split("/")[0] not in allowed_types:
        logging.warning("Unauthorized upload - content type not allowed")
        raise HTTPException(status_code=401, detail="Unauthorized")

    id = ''.join(random.choices(string.ascii_lowercase, k=APP_ID_LEN))
    filename = id+"-"+file.filename
    with open("files/"+filename, "wb") as f:
        f.write(file.file.read())
    logging.info(f"Successfully uploaded file '{filename}' to server")

    link = "https://" + APP_DOMAIN + "/file/" + filename
    return templates.TemplateResponse("done.html", {"request": request, "link": link})

@app.get("/file/{filename}", response_class=FileResponse)
def get_file(filename: str, request: Request):
    return "files/" + filename


# RUNNER & EXCEPTION HANDLER ############################

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
