## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Project Description

Provide an overview of your project, its purpose, and its main functionalities. For example, this project is a real-time chat application where users can communicate with each other in real-time.

## Features

- Real-time chat functionality using WebSocket communication
- User authentication and authorization
- Sending and receiving messages between users
- Displaying online/offline status of users
- Search and filter users

## Technologies Used

- Django: Python web framework for backend development.
- Django Channels: Provides WebSocket communication capabilities for real-time updates.
- Django Rest Framework: Used for building RESTful APIs.
- Vue.js: JavaScript framework for building interactive UI components.
- Tailwind CSS: Utility-first CSS framework for styling the application.

## Installation

## Clone the repository:

   git clone <repository_url>


## Navigate to the project directory:
    cd <project_directory>

## Create a virtual environment:

    python3 -m venv venv
##  Activate the virtual environment:
    source venv/bin/activate

## Install the Python dependencies:
pip install -r requirements.txt
Install the Node.js dependencies for the frontend:



## Start the Django development server:
    daphne base.asgi:application

## In a separate terminal, start the Vue.js development server:

    cd frontend
    npm run serve

## Access the application in your web browser:
http://localhost:8000


API Documentation

The API endpoints provided by the application are as follows:

/api/v1/users/: GET endpoint to fetch the list of users.
/api/v1/fetch-chat-messages/<sender_username>/<recipient_username>/: GET endpoint to fetch the chat messages between the sender and recipient.
Please refer to the API documentation for more details on the request/response formats and authentication requirements.



Contributing
Contributions are welcome! If you want to contribute to this project, please follow these steps:

Fork the repository.
Create a new branch for your feature/bug fix.
Make your changes and commit them.
Push your changes to your forked repository.
Submit a pull request.
Please make sure to follow the coding style and write meaningful commit messages.

License
Specify the license under which your project is distributed. For example, this project is licensed under the MIT License. You can include the license text or provide a link to the license file.


Feel free to customize this README file further by adding more sections or adjusting the content according to your project's specific details and requirements.