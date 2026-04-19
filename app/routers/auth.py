from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from passlib.context import CryptContext
from app.database import get_db, execute_with_sql
from app import models
from app.models import User, UserRole
from app.schemas import UserCreate, Token, ClientUserCreate
from sqlalchemy import select, func

router = APIRouter(tags=["auth"])

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    stmt = select(models.User).where(models.User.username == username)
    user = db.execute(stmt).scalars().first()
    if user is None:
        raise credentials_exception
    return user

def require_role(*roles: UserRole):
    def check_role(current_user = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Unauthorized access")
        return current_user
    return check_role


@router.get("/auth/users")
def get_all_users(db:Session = Depends(get_db), current_user = Depends(require_role(UserRole.admin))):
    stmt = select(models.User)
    return execute_with_sql(db, stmt, False)

@router.post("/auth/register", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    stmt = select(models.User).where(models.User.username == user.username)
    result = db.execute(stmt).scalars().first()
    if result:
        raise HTTPException(status_code=400, detail="User already exists.")


    db_user = models.User(
        username=user.username,
        hashed_password=hash_password(user.password),
        role = user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"username": db_user.username}

@router.post("/auth/login", status_code=200)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    stmt = select(models.User).where(models.User.username == form_data.username)
    result = db.execute(stmt).scalars().first()
    if not result:
        raise HTTPException(status_code=401, detail="User doesnt't exists.")
    
    if not verify_password(form_data.password, result.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    token = create_access_token({"sub": result.username})

    return {"access_token": token, "token_type": "bearer"}



@router.post("/auth/users/clients")
def add_client_to_user(new_connection: ClientUserCreate, db: Session = Depends(get_db), 
                       current_user = Depends(require_role(UserRole.admin, UserRole.employee)) ):
    
    #check if client user
    user_stmt = select(models.User).where(models.User.username == new_connection.username)
    user_result = db.execute(user_stmt).scalars().first()
    if not user_result:
        raise HTTPException(status_code=404, detail="User ID doesnt't exists.")
    

    userid = user_result.id
    
    #check if client exists
    client_stmt = select(models.Client).where(models.Client.client_id == new_connection.client_id)
    client_result = db.execute(client_stmt).scalars().first()
    if not client_result:
        raise HTTPException(status_code=404, detail="Client ID doesnt't exists.")
    
    clientid = client_result.id
    
    #check for user limit
    if user_result.role == UserRole.client_user:
        check_client_limit = select(func.count()).select_from(models.UserClient).where(models.UserClient.user_id == userid)
        check_client_limit_result = db.execute(check_client_limit).scalars().one()
        if check_client_limit_result >= 1:
            raise HTTPException(status_code=409, detail="Client User cannot have more 1 conneted client")
    
    

    #check for existing connection
    existing_connection = select(models.UserClient).where(
        models.UserClient.user_id == userid, models.UserClient.client_id == clientid)

    existing_connection_result = db.execute(existing_connection).scalars().first()
    
    if existing_connection_result:
        raise HTTPException(status_code=409, detail="User is already assigned to this client.")
    


    db_userclient = models.UserClient(user_id = userid, client_id = clientid)

    db.add(db_userclient)
    db.commit()
    db.refresh(db_userclient)
    return db_userclient

@router.post("/auth/users/connection")
def see_all_connection(db: Session = Depends(get_db), 
                       current_user = Depends(require_role(UserRole.admin))):
    
    stmt = select(models.UserClient)
    results = db.execute(stmt).scalars().all()
    output = []
    for connection in results:
        output.append({
            "id": connection.id,
            "username": connection.user_table.username,
            "user_role": connection.user_table.role,
            "client_id": connection.client_table.client_id
        })
    
    return output


    # return execute_with_sql(db, stmt, False)


@router.post("/auth/users/client/connection")
def see_user_connection(user_id: Optional[str], db: Session = Depends(get_db), 
                       current_user = Depends(require_role(UserRole.admin, UserRole.employee, UserRole.client_user))):
    
    stmt = select(models.UserClient).where(models.UserClient.user_id == current_user.id)
    
    if user_id: 
        stmt = select(models.UserClient).where(models.UserClient.user_id == user_id)
    
    results = db.execute(stmt).scalars().all()
    output = []
    for connection in results:
        output.append({
            "id": connection.id,
            "username": connection.user_table.username,
            "user_role": connection.user_table.role,
            "client_id": connection.client_table.client_id
        })
    
    return output