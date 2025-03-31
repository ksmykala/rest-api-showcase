# REST API Showcase

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.0-green)

## Description

The **REST API Showcase** project demonstrates the implementation of a RESTful API using Flask. It serves as a foundational template for building scalable and maintainable web services, incorporating best practices and a modular architecture.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Modular Design**: Organized project structure promoting scalability and maintainability.
- **User Authentication**: JWT-based authentication system for secure API access.
- **Docker Support**: Containerization using Docker for consistent development and deployment environments.
- **Database Integration**: SQLAlchemy for ORM-based database interactions.
- **Input Validation**: Marshmallow schemas for validating incoming data.
- **Error Handling**: Custom error responses for enhanced API reliability.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ksmykala/rest-api-showcase.git
   cd rest-api-showcase
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Rename `.env.example` to `.env` and configure the necessary environment variables.

5. **Initialize the database**:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Run the application**:
   ```bash
   flask run
   ```

   The API will be accessible at `http://127.0.0.1:5000/`.

   or run it as a docker container using:
   ```
   docker compose up --build -d
   ```
   The API will be accessible at `http://127.0.0.1:5005/`

## Usage

After setting up the project, you can interact with the API using tools like [Postman](https://www.postman.com/), [Insomnia](https://insomnia.rest/) or `curl`. Below is an example of how to register a new user:

```bash
curl -X POST http://127.0.0.1:5000/register \
     -H "Content-Type: application/json" \
     -d '{"username": "newuser", "password": "password123"}'
```

For detailed information on available endpoints and their usage, refer to the [API Endpoints](#api-endpoints) section below.

## API Endpoints

The API provides, among others, the following endpoints:

- **User Registration**: `POST /register`
  - Registers a new user.
  - **Request Body**:
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "User created successfully."
    }
    ```

- **User Login**: `POST /login`
  - Authenticates a user and returns an access token.
  - **Request Body**:
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
  - **Response**:
    ```json
    {
      "access_token": "string"
    }
    ```

- **Protected Resource**: `GET /protected`
  - Accesses a resource that requires authentication.
  - **Headers**:
    ```bash
    Authorization: Bearer <access_token>
    ```
  - **Response**:
    ```json
    {
      "message": "This is a protected resource."
    }
    ```

*Note: Replace `<access_token>` with the token obtained from the login endpoint.*

## Acknowledgements

This repository was created based on a course "REST APIs with Flask and Python" conducted by [Jose Salvatierra](https://github.com/jslvtr). Many thanks to the author for providing valuable educational content that inspired the development of this project.



## Contact

For questions or inquiries, please contact:
[Krzysztof Smykała](mailto:k.smykala@gmail.com)