from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Depends, FastAPI, Header, HTTPException, Request

from jose import JWTError, jwt
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from fastapi import Header

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime, timedelta



app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "5a24b3e8b0f0ea588cf1ee6f7bee0b37fe9f84e6f2587db90ae2d31442febb0a"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 10
now = datetime.utcnow()

def create_access_token(data: dict):
    to_encode = data.copy()
    created = int(now.strftime('%s'))
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"created": created, "exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt




@app.get("/headers-1/")
async def create_headers(response: Response, request: Request):
    user = {
        "name": "John",
        "age": 30,
        "is_student": True,
    }
    token = create_access_token(user)
    response.set_cookie(key="token", value=token, httponly=True, max_age=3600) # 3600 = 60 minutes
    
    headers = dict(request.headers)
    return {"headers": headers}


@app.get("/headers-2/")
async def read_headers(request: Request):
    token = request.cookies.get("token")
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    # validate the token and do other stuff
    
    headers = dict(request.headers)
    return {"headers": headers}


@app.get("/delete-cookie")
async def delete_cookie(response: Response, request: Request):
    response.delete_cookie("token")
    # response.delete_cookie("token_type")
    
    headers = dict(request.headers)
    return {"headers": headers}



# async def get_token_header(token: str = Header(...)):
#     if token != "secret-token":
#         raise HTTPException(status_code=400, detail="Invalid token")
#     return token


# @app.get("/items/")
# async def read_items(request: Request):
#     token: str = Depends(get_token_header)
#     return {"token": token}


# Print whole header
# @app.get("/headers-1/")
# async def create_headers(request: Request):
#     headers = dict(request.headers)
#     user = {
#         "name": "John",
#         "age": 30,
#         "is_student": True,
#     }
#     # print(user["name"]) # Output: John

#     token = create_access_token(user)
    
#     # Add a new header to the dictionary
#     headers["user"] = user["name"]
#     headers["token"] = token
#     headers["token"] = token
    
#     return {"headers": headers}


# @app.get("/headers-2/")
# async def read_headers(request: Request):
#     headers = dict(request.headers)
    
    
#     return {"headers": headers}
