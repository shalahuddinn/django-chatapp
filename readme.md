# Overview

ChatApp is a REST API build by using the Django Rest Framework. My environment:

1. Python 3.9.0
2. Django 3.1.4 Final
3. Django REST Framework 3.12.2

## Usage

1. Install all the packages above in a virtual environment or global environment. In case of using virtual environment, do not forget to activate it first.
2. change directory to this root project (cd command).
3. run the django server

```bash
python manage.py runserver
```

4. For add or remove data into database/model, you can use django admin page or access the Model/Data Manipulation page

#### django admin page superuser information

```
username=admin
password=admin
```

#### Model/Data manipulation page URL. CRUD operation can be done on the page.

```
# Retrieve, create, update or delete a User model.
/data/user/

# Retrieve, create, update or delete a Message model.
/data/message/

# Retrieve, create, update or delete a Conversation model.
/data/conversation/
```

# Use case scenario

## 1. Create user first.

#### `POST /api/user/register/`

##### Request

```json
{
  "username": "bangjago",
  "email": "bangjago@bangjago.com",
  "password": "bangjago"
}
```

##### Response

```json
{
  "id": 2,
  "username": "bangjago",
  "email": "bangjago@bangjago.com",
  "token": "6a77d071c456898b679b1d504e14c9edc9fff0dc"
}
```

## 2. If you forget the token, you can get the token by login. (1 User = 1 Token)

#### `POST /api/user/login/`

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
  "token": "6a77d071c456898b679b1d504e14c9edc9fff0dc"
}
```

## 3. Get a list of all of the conversations that a user participate

#### `GET /api/conversation/user/`

##### Request

Header

```
/* DO NOT FORGET TO PUT A SPACE CHARACTER AFTER 'Token' word. */
Authorization: Token 6a77d071c456898b679b1d504e14c9edc9fff0dc
```

##### Response

```json
[
  {
    "id": 1,
    "participants": ["bangjago", "bangjago2"],
    "last_message": {
      "message": "halo bangjago2",
      "timestamp": "2020-12-05T08:12:00.248979Z"
    },
    "unread_count": 0
  },
  {
    "id": 2,
    "participants": ["bangjago", "bangjago3"],
    "last_message": null,
    "unread_count": 0
  }
]
```

## 4. Create a conversation

#### `POST /api/conversation/create/`

##### Request

Header

```json
/* DO NOT FORGET TO PUT A SPACE CHARACTER AFTER 'Token' word */
Authorization: Token 6a77d071c456898b679b1d504e14c9edc9fff0dc
```

Body

User who made the request should be in the participants list.
Format: [<username1>, <username2>]

```json
{
  "participants": ["bangjago", "bangjago2"]
}
```

##### Response

```json
{
  "id": 1,
  "participants": ["bangjago", "bangjago2"]
}
```

## 5. Get all messages in a conversation

#### `GET api/conversation/<int:pk>/message/` (pk is the conversation id)

##### Request

Header

```json
/* DO NOT FORGET TO PUT A SPACE CHARACTER AFTER 'Token' word */
Authorization: Token 6a77d071c456898b679b1d504e14c9edc9fff0dc
```

##### Response

```json
[
  {
    "id": 1,
    "conversation_id": 1,
    "sender": "bangjago",
    "message": "halo bangjago2",
    "timestamp": "2020-12-05T08:12:00.248979Z",
    "is_read": false
  }
]
```

## 6. Send a message in a conversation

#### `POST api/conversation/<int:pk>/message/` (pk is the conversation id)

##### Request

Header

```json
/* DO NOT FORGET TO PUT A SPACE CHARACTER AFTER 'Token' word */
Authorization: Token 6a77d071c456898b679b1d504e14c9edc9fff0dc
```

Body

```json
{
  "message": "halo bangjago2"
}
```

##### Response

```json
{
  "id": 1,
  "conversation_id": 1,
  "sender": "bangjago",
  "message": "halo bangjago2",
  "timestamp": "2020-12-05T08:12:00.248979Z",
  "is_read": false
}
```
