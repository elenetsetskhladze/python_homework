from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserLogin, UserUpdate, RefreshTokenSchema
from app.database import get_db
from app.models.user import User
from app.security import verify_password, hash_password, get_current_user, require_admin, create_access_token, create_refresh_token, SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/user", tags=["users"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user:UserCreate , db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    data = user.model_dump(exclude = {"password", "confirm_password"})

    new_user = User(**data, hashed_password = hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    if not verify_password(
        form_data.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(
        data={"user_id": existing_user.id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/token/refresh")
def refresh_token(request: RefreshTokenSchema):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")
        token_type = payload.get("token_type")

        if not user_id or token_type != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = create_access_token(data={"user_id": user_id})

    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.username = data.username
    current_user.email = data.email

    db.commit()
    db.refresh(current_user)

    return current_user

@router.get("/", response_model=list[UserResponse])
def get_users(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(User).all()

    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user

@router.patch("/{user_id}/make_admin")
def make_admin(user_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.role == "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already an admin")

    user.role = "admin"
    db.commit()
    db.refresh(user)

    return {
        "message": f"User {user.username} is now an admin!"
    }

@router.patch("/{user_id}/remove_admin")
def remove_admin(user_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot remove your own admin privileges")

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.role == "user":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not an admin")

    user.role = "user"
    db.commit()
    db.refresh(user)

    return {
        "message": f"Admin privileges removed from user {user.username}"
    }

@router.delete("/{user_id}")
def delete_user(user_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()

    return {
        "message": f"User {user.username} deleted successfully"
    }





