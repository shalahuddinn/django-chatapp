# Overview

ChatApp is a REST API build by using the Django Rest Framework. My environment:

1. Python 3.9.0
2. Django 3.1.4 Final
3. Django REST Framework 3.12.2

## Usage

1. Install all the packages above in a virtual environment or global environment. In case of using virtual environment, do not forget to activate it first.
2. change directory to this root project. (cd command).
3. run the django server

```bash
python manage.py runserver
```

4. For add or remove data into database, better to use django admin page. `/admin/`

```
username=admin
password=admin
```

# 1. Use case scenario

## Create user first.

#### `POST /api/users/register/`

This endpoint is opened in public.

##### Request

```json
{
  "username": "bangjago",
  "email": bangjago@bangjago.com,
  "password": "bangjago"
}
```

##### Response

```json
{
  "id": 10,
  "username": "bangjago",
  "email": "bangjago@bangjago.com",
  "token": "37baa65bdf296445b76c39dd101550adf4fe03fd"
}
```

## 2. If you forget the token, you can get the token by login. (1 User = 1 Token)

#### `POST /api/users/login/`

This endpoint is opened in public.

##### Request

```json
{
  "username": "bangjago",
  "password": "bangjago"
}
```

#### Response

```json
{
  "token": "37baa65bdf296445b76c39dd101550adf4fe03fd"
}
```

## 3. Get list all of the conversations that a user has

#### `GET /api/conversations/users/`

##### Request

Header

```json
/* DO NOT FORGET TO PUT A SPACE CHARACTER AFTER 'Token' word */
Authorization: Token 37baa65bdf296445b76c39dd101550adf4fe03fd
```

Body

```json
{}
```

##### Response

```json
[
  {
    "id": 1,
    "participants": [
      {
        "id": 6,
        "username": "bangjago2"
      },
      {
        "id": 10,
        "username": "bangjago"
      }
    ],
    "last_message": {
      "message": "punten",
      "timestamp": "2020-12-03T10:22:22.454937Z"
    }
  },
  {
    "id": 2,
    "participants": [
      {
        "id": 8,
        "username": "bangjago3"
      },
      {
        "id": 10,
        "username": "bangjago"
      }
    ],
    "last_message": null
  }
]
```

## 4. Create a conversation

#### `POST /api/conversations/`

##### Request

Header

```json
/* DO NOT FORGET TO PUT A SPACE CHARACTER AFTER 'Token' word */
Authorization: Token 37baa65bdf296445b76c39dd101550adf4fe03fd
```

Body

```json
{
  /* Format: [<username1>, <username2>] 
  User who made the request should be in the participants list */
  "participants": ["bangjago", "bangjago2"]
}
```

##### Response

```json
{
  "id": 12,
  "participants": ["bangjago2", "bangjago"]
}
```

## 5. Get messages in a conversations

#### `GET api/conversations/<int:pk>/messages/` (pk is the conversation id)

##### Request

Header

```json
/* DO NOT FORGET TO PUT A SPACE CHARACTER AFTER 'Token' word */
Authorization: Token 37baa65bdf296445b76c39dd101550adf4fe03fd
```

Body

```json
{}
```

##### Response

```json
{}
```
