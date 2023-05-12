# **Student REST API**

 This is a simple Flask REST API that allows you to save and retrieve single or multiple student records from a MySQL database. 

 It also includes rate limiting & authentication features & uses Redis as a cache to speed up subsequent requests. The application is fully dockerized & containerized.


 ## **Requirements**
___

- Python 3.9 + 
- Docker
- MySql
- Docker Compose File
- Redis

 ## **Getting Started**

___
 - Clone the repository to your local machine.
 - Install Docker on the local Machine. 
 - Create a filed named  `.env` in the current local directory.

 - Add all of the following enviroment variable in the `.env` file with proper value:  
    - DB_URL `( eg : mysql+pymysql://user:password@db/db_name )`
    - SECRET_KEY
    - MYSQL_ROOT_PASSWORD
    - MYSQL_DATABASE
    - MYSQL_USER
    - MYSQL_PASSWORD

 - Start the application with **`docker-compose up --build`** on terminal.
- This will start the server on [Localhost](http://localhost:5000) using the default port of flask which is port: 5000.


## **Usage**
___

### *Endpoints :*

<br>

1. `POST /signup`

    - This endpoint will create a user , So we can use it to login.

    Request Body:
    ``` 
    {
    "username": "Example",
    "password": "1jada232#",
    }
    ```
    The rendered output looks like this:
    ```
    {
        "success": "new user has been created."
    }
    ```
<br>

2.  `POST /login`

    - This endpoint will login a user , first we need to create a user if we haven't.

    Request Body:
    ``` 
    {
    "username": "Example",
    "password": "1jada232#",
    }
    ```
    The rendered output looks like this:
    ```
    {
        "success": "User authenticated sucessfully."
    }
    ```
<br>

3. `GET /logout`

    - This endpoint will logout a user , If they are logged in.

    The rendered output looks like this:
    ```
    {
    "success": "User sucessfully logged out."
    }
    ```
<br>

4. `POST /student/create`

    - This endpoint will create a user , We need to be logged in to perform this action.

    Request Body:
    ``` 
    {
    "name": "Example",
    "age": "15",
    "standard": "9th",
    "rollnumber": "26",
    }
    ```
    The rendered output looks like this:
    ```
    {
        "age": 15,
        "id": 1,
        "name": "Example",
        "rollnumber": 26,
        "standard": "9th"
    }
    ```
<br>

5. `GET /student/<int:id>`

    - This endpoint will fetch a user with the provided ID in the url , We need to be logged in to perform this action.

    The rendered output looks like this:
    ```
    {
        "age": 15,
        "id": 1,
        "name": "Example",
        "rollnumber": 26,
        "standard": "9th"
    }
    ```
<br>

6. `GET /students`

    - This endpoint will fetch all the user from the DB or Cache , We need to be logged in to perform this action.

    The rendered output looks like this:
    ```
    {
        {
            "age": 15,
            "id": 1,
            "name": "Example",
            "rollnumber": 26,
            "standard": "9th"
        }
        {
            "age": 17,
            "id": 2,
            "name": "Example2",
            "rollnumber": 12,
            "standard": "11th"
        }
    }
    ```



## **Rate Limiting**
___

This application includes rate limiting to ensure that not more than 1 request per minute can be sent to the API. If you attempt to send too many requests, you will receive an error message.

## **Authentication**
___

This application also includes authentication to ensure that only authorized users can access the API. You will need to use login API to login to get access to all other API endpoints.

## **Error Codes**
___

The following error codes are returned by the API:

- **200 OK**: The request has succeeded.
- **201 Created**: The request has succeeded and has led to the creation of a resource..
- **400 Bad Request**: The request body is invalid.
- **401 Unauthorized**: The request is not authenticated.
- **404 Not Found**: The resource does not exist.
- **429 Too Many Requests**: The user has sent too many requests in a given amount of time.

- **500 Internal Server Error**: An unexpected error occurred.


