from fastapi import FastAPI, Form, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse


from starlette import status

from pymongo.errors import PyMongoError
from typing import Annotated

from db import check_exist, user_collection
from model import UserInDb
from auth import password_hash, create_token, current_user, authenticate_form_db

app = FastAPI()


# @app.post('/users/logins')
# async def users_login(response: Response,
#                       current_user_check: Annotated[bool, Depends(current_user)],
#                       username: str = Form(..., min_length=6),
#                       password: str = Form(..., min_length=6),):
#
#     if not username or not password:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="please fill the login form")
#     if not current_user_check:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     if authenticate_form_db(username=username,password=password):
#         access_token = create_token(data={'sub': username})
#         response.set_cookie(key='auth_cookie', value=access_token)
#         return {'detail': 'login successful'}
#     return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something went wrong')


@app.post('/users/register')
async def users_register(response: Response,
                         username: str = Form(...),
                         email: str = Form(...),
                         password1: str = Form(...),
                         password2: str = Form(...),):

    if not username or not email or not password1 or not password2:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'massage': 'please fill the form'})
    if password1 != password2:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'massage': 'passwords dont match'})
    form_data = UserInDb(username=username,
                         email=email,
                         hs_password=password1)
    if not check_exist(form_data.username):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'massage': 'user already exist'})
    hashed_pass = password_hash.hash(password1)
    form_data.hs_password = hashed_pass
    try:
        user_collection.insert_one(dict(form_data))
    except PyMongoError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'massage': 'Something went wrong'})

    access_token = create_token(data={'sub': form_data.username})
    response.set_cookie(key='auth_cookie', value=access_token)
    return {'massage': 'register was successful'}


@app.post('/users/logout')
async def users_logout(request: Request,
                       response: Response):
    response.delete_cookie(key='auth_cookie')
    return {'detail': 'successfuly logout'}


@app.post('/users/logins')
async def users_login(response: Response,
                      username: str = Form(..., min_length=6),
                      password: str = Form(..., min_length=6),):

    if not username or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="please fill the login form")
    if authenticate_form_db(username=username,password=password):
        access_token = create_token(data={'sub': username})
        response.set_cookie(key='auth_cookie', value=access_token)
        return {'detail': 'login successful'}
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something went wrong')


# token: Annotated[TokenModel, Depends(current_user)]
@app.get('/users/test')
async def test(request: Request):
    if request.cookies.get('auth_cookie'):
        return {'cookie':request.cookies.get('auth_cookie'),
                'ok': 'ok'}
    return
