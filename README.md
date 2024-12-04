# Generic Authentication/Authorization Template in FastAPI

## Description

This project is a **generic authentication and authorization template** built with FastAPI. It provides a secure foundation for user management in any application, including user registration, login, and token-based authentication. The project uses SQLite for simplicity but can be extended to support other databases.

## Authentication Technology

This template implements **JWT (JSON Web Tokens)** for authentication:

- **Password Security**: Uses `bcrypt` hashing for secure password storage.
- **Token Handling**: Generates and decodes JWT tokens using `jose` library. Tokens include expiration to enhance security.
- **OAuth2 Integration**: Employs FastAPI's `OAuth2PasswordBearer` to manage token-based authorization.

## Features

- **User Registration**: Handles unique username and email constraints.
- **Login**: Validates credentials and issues JWT tokens.
- **Current User Retrieval**: Provides APIs to fetch details of the currently authenticated user.
- **Protected Routes**: Implements dependency injection to secure routes.

## Getting Started

### Prerequisites

- Python 3.7+
- Virtual environment setup (optional but recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MohamedFarouk94/Auth-FastAPI
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

### Configuration

1. **Database**: By default, the app uses SQLite. Update `DATABASE_URL` in `database.py` for other databases.

2. **Secret Key**: Replace `YOUR_SECRET_KEY` in `auth.py` with:
   ```python
   SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
   ```

3. **Token Expiration**: Adjust `ACCESS_TOKEN_EXPIRE_MINUTES` in `auth.py` as per requirements.

4. **Models and Schemas**: Update `models.py` and `schemas.py` to include new fields or features.

5. **Secure the `do_action` API**: Modify the function in `main.py` to include desired execution logic. Or of course you can add other similar functions to execute authorized actions, Here's how `do_action` is implemented:
   ```python
   @app.get("/users/{username}/")
    def do_action(username: str, current_user: models.User = Depends(auth.get_current_user)):
        if current_user.username != username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden"
            )
        #
        # EXECUTE ACTIONS HERE
        #
        return {'message': 'ok'}    # Change it to the desired response
   ```

## Usage

1. **Register a User**:
   - Endpoint: `POST /register/`
   - Payload:
     ```json
     {
       "username": "testuser",
       "password": "password123",
       "email": "test@example.com"
     }
     ```

2. **Login**:
   - Endpoint: `POST /login/`
   - Payload:
     ```json
     {
       "username": "testuser",
       "password": "password123"
     }
     ```
   - Response:
     ```json
     {
       "access_token": "JWT_TOKEN_HERE",
       "token_type": "bearer"
     }
     ```

3. **Access Protected Endpoints**:
   - Pass the token in the `Authorization` header:
     ```
     Authorization: Bearer JWT_TOKEN_HERE
     ```

   - Example protected endpoint: `GET /users/me/` which responds with the the `UserResponse` schema. Here's the `read_current_user` function in `main.py`: 
    ```python
        @app.get("/users/me/", response_model=schemas.UserResponse)
        def read_current_user(current_user: models.User = Depends(auth.get_current_user)):
            return current_user
    ```
    - And you can access protected endpoints defined with `do_actions` and your customized functions.
