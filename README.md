
# WhatsApp Assistant

This project is a FastAPI-based implementation of a WhatsApp Assistant using OpenAI's API. The assistant is designed to help guests staying in an Airbnb in Paris by responding to their queries using a pre-defined knowledge base. The assistant is friendly, helpful, and provides guidance where possible.

## Table of Contents

- [Setup](#setup)
- [Environment Variables](#environment-variables)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Setup

To get started with this project, you'll need to follow the steps below to set up your environment and run the application.

### Environment Variables

Create a `.env` file in the root directory of your project and set the following environment variables:

```plaintext
ACCESS_TOKEN=
APP_ID=
APP_SECRET=
RECIPIENT_WA_ID=
VERSION=
PHONE_NUMBER_ID=
VERIFY_TOKEN=

OPENAI_API_KEY=your_openai_api_key
OPENAI_ASSISTANT_ID=your_openai_assistant_id
```

- `ACCESS_TOKEN`: The access token for the WhatsApp API.
- `APP_ID`: The application ID for the WhatsApp API.
- `APP_SECRET`: The application secret for the WhatsApp API.
- `RECIPIENT_WA_ID`: Your phone number with the country code (e.g.`+26377000000`).
- `VERSION`: The version of the WhatsApp API.
- `PHONE_NUMBER_ID`: The phone number ID for the assistant.
- `OPENAI_API_KEY`: Your OpenAI API key used to authenticate requests.
- `OPENAI_ASSISTANT_ID`: The ID of the assistant created through OpenAI.

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/panda-zw/fastapi-whatsapp-openai.git
    cd fastapi-whatsapp-openai
    ```

2. **Set up a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Load environment variables:**

    Ensure your `.env` file is properly set up with your OpenAI credentials.

## Usage

### Running the Application

To run the FastAPI application, use the following command:

```bash
fastapi dev run
```

This will start the server on `http://127.0.0.1:8000`.

### Managing the Assistant

The assistant interacts with the WhatsApp API, processing incoming messages and generating appropriate responses based on the knowledge base provided.

### Key Features

- **Message Processing:** The assistant can process incoming messages and respond accordingly.
- **Thread Management:** Handles multiple conversation threads with users, storing thread IDs for ongoing conversations.
- **Error Handling:** Implements error handling to manage issues such as API connection errors and active run conflicts.

## API Endpoints

### `/send_test_message`

- **Method:** `POST`
- **Description:** Sends a test message to the WhatsApp API. If you are in test mode make sure you reply to this message to continue receiving messages.
- **Response:** Returns a success message if the message is sent successfully.


### `/webhooks`

- **Method:** `POST`
- **Description:** Receives incoming WhatsApp messages and processes them using the assistant.
- **Response:** Returns the assistant's response or an error message if the processing fails.

### `/webhooks

- **Method:** `GET`
- **Description:** Verifies the webhook endpoint with the WhatsApp API.
- **Response:** Returns a challenge response to verify the endpoint.

### Helper Functions

- **upload_file(path):** Uploads a file to the assistant's knowledge base.
- **create_assistant(file):** Creates a new assistant instance using the provided file.
- **check_if_thread_exists(wa_id):** Checks if a thread exists for the given WhatsApp ID.
- **store_thread(wa_id, thread_id):** Stores the thread ID associated with a WhatsApp ID.
- **run_assistant(thread, name):** Runs the assistant to generate a response based on the user's message.

## Error Handling

### Common Errors

- **APIConnectionError:** Handles connectivity issues with the OpenAI API.
- **TimeoutError:** Raised when waiting for a response from the assistant takes too long.
- **BadRequestError:** Occurs when there is an issue with the request sent to the OpenAI API.

### Logging

Logging is implemented to track the status of assistant runs and errors encountered during processing.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome all contributions!

### Steps to Contribute

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push your branch to your forked repository.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
