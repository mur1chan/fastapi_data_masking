# FastAPI Data Masking

## Introduction

This repository contains a FastAPI project developed for a university course. The primary aim of this API is to pseudonymize, anonymize, and encrypt data. This project provides a robust, secure, and straightforward way to manipulate sensitive data, making it suitable for academic and research purposes.

## Security Measures

The project aims to incorporate several layers of security to ensure the safe transfer of data between the client and the API:

- **HTTPS**: Implementation is planned for secure communication.
- **Bearer Token Authentication**: Access to the API is restricted to users who provide a valid Bearer token.

Note: Current work is ongoing to improve these aspects. For more information, check out the project's security checklist below.

## Installation & Setup

As the project is still in development, specific installation instructions are not available yet. However, the application will be Dockerized for easy deployment and added security.

### Prerequisites

- Python 3.x
- FastAPI
- Uvicorn

### API Endpoints

- `POST /token`: For obtaining the Bearer token.
- `POST /create_db/somerandomstrings`: To create a database.
- `POST /customer/{customer_name}`: To insert a new customer record after pseudonymizing the data.
- `DELETE /customer/{customer_name}`: To delete a customer record.
- `PUT /customer/{customer_name}`: To update customer details.

### Authentication

The API uses Bearer Token Authentication. Tokens are generated upon successful login, and they must be included in the header for accessing protected routes.

### Libraries Used

- **FastAPI**: For creating the API.
- **OAuth2PasswordBearer**: For implementing OAuth2 password flow.
- **Cryptography**: Python cryptography library used for encryption (Fernet).

## Security Checklist

- [ ] Implement HTTPS for secure data transmission between the client and the API.
- [ ] Setup the Docker container with proper security measures.

## Contributing

Since this is a university project, contributions are limited to team members. However, feedback is always welcome.
