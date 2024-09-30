# WA Driver Guide Practice API

This repository contains the backend API for an application designed to help native Chinese speakers study the Washington Driver Guide for their knowledge test required to obtain a driver's license. The API leverages GPT-4 by OpenAI to generate questions based on the Washington Driver Guide.

The API is built using the FastAPI framework, which is known for its performance and ease of use. It also uses Turso as the database solution and asyncio for asynchronous database operations.

Deployments and Links:

- Frontend repository [link](https://github.com/adamowada/wa-driver-guide-practice-frontend)
- Frontend deployment on Vercel [link](https://wa-driver-guide-practice-frontend.vercel.app/)
- API repository [link](https://github.com/adamowada/wa-driver-guide-practice-api)
- API deployment on Vercel [link](https://wa-driver-guide-practice-api.vercel.app/)

## Table of Contents

1. [Getting Started](#getting-started)
2. [Technologies Used](#technologies-used)
3. [Configuration](#configuration)
4. [API Documentation](#api-documentation)
   - [Get Questions](#get-questions)
   - [Create Questions](#create-questions)
5. [Error Handling](#error-handling)
6. [Deployment](#deployment)
7. [Contributing](#contributing)

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Python (v3.7 or later)
- `pip` package manager

### Installation

Clone the repository:

```bash
git clone https://github.com/adamowada/wa-driver-guide-practice-api.git
cd wa-driver-guide-practice-api
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the API Locally

You can start the API server with the following command:

```bash
uvicorn api.get_questions:app --reload
# or
uvicorn api.create_questions:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **OpenAI GPT-4**: Used for generating questions based on the Washington Driver Guide.
- **Turso**: Utilized as the database solution for storing questions and answers.
- **asyncio**: For asynchronous operations to handle database transactions efficiently.
- **Vercel**: Deployment platform for serverless applications.

## Configuration

Create a `.env` file in the root directory and add your API keys and other configurations:

```env
OPENAI_API_KEY=<your_openai_api_key>
TURSO_DB_URL=<your_turso_db_url>
TURSO_DB_AUTH_TOKEN=<your_turso_db_auth_token>
```

## API Documentation

### Get Questions

- **Endpoint**: `/api/get-questions`
- **Method**: `GET`

#### Request

This endpoint does not require any parameters.

#### Response

- **Status**: `200 OK`
- **Body**: JSON array of the questions and answers.

Example:

```json
{
  "questions": [
    {
      "question": "Question text...",
      "answers": [
        {
          "text": "Answer text...",
          "correct": true,
          "explanation": "Explanation text..."
        },
        {
          "text": "Answer text...",
          "correct": false,
          "explanation": "Explanation text..."
        }
      ],
      "image_url": "http://example.com/image.png"
    }
  ]
}
```

### Create Questions

- **Endpoint**: `/api/create-questions`
- **Method**: `POST`

#### Request

This endpoint does not require any parameters.

#### Response

- **Status**: `201 Created`
- **Body**: JSON array of the created questions and answers.

Example:

```json
{
  "questions": [
    {
      "question": "Question text...",
      "answers": [
        {
          "text": "Answer text...",
          "correct": true,
          "explanation": "Explanation text..."
        },
        {
          "text": "Answer text...",
          "correct": false,
          "explanation": "Explanation text..."
        }
      ],
      "image_url": "http://example.com/image.png"
    }
  ]
}
```

## Error Handling

The API will return standard HTTP status codes to indicate the success or failure of an API request. Common status codes include:

- `200 OK`: The request was successful.
- `201 Created`: The resource was successfully created.
- `400 Bad Request`: The request could not be understood or was missing required parameters.
- `401 Unauthorized`: Authentication failed or user does not have permissions for the requested operation.
- `404 Not Found`: The requested resource could not be found.
- `500 Internal Server Error`: An error occurred on the server.

## Deployment

### Vercel

This API is configured to be deployed on Vercel. The `vercel.json` file includes the necessary configurations. To deploy, follow these steps:

1. Install Vercel CLI if you haven't already:

   ```bash
   npm install -g vercel
   ```

2. Deploy the project:

   ```bash
   vercel
   ```

## Contributing

Contributions are welcome! If you have any ideas or improvements, please open an issue or submit a pull request.
