
# SnuggPro Automation Project

This project is a Flask-based application that integrates with Monday.com to automate tasks related to SnuggPro job creation. The application receives and processes webhooks from Monday.com, retrieves item data, and creates jobs through the SnuggPro API.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Running with Docker](#running-with-docker)
- [Local Development with ngrok](#local-development-with-ngrok)
- [Deploying to Google Cloud Run](#deploying-to-google-cloud-run)
- [Updating Versions and Environment Variables on GCP](#updating-versions-and-environment-variables-on-gcp)
- [Testing](#testing)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The SnuggPro Automation Project simplifies job creation by integrating with Monday.com and SnuggPro's APIs. It listens for webhook events, processes the data, and creates jobs accordingly. This solution helps streamline workflows and reduce manual data entry.

## Features

- Listens for webhooks from Monday.com
- Retrieves item data via Monday.com GraphQL API
- Converts item data for SnuggPro job creation
- Uses Flask as a web server
- Integrates with the SnuggPro API for job management

## Installation

### Local Development Setup

For local development, you will need to install dependencies manually using `requirements.txt`.

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```
2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running with Docker

Using Docker means you don't need to install dependencies locally; the setup is automated in the Docker container.

## Configuration

1. Create a `.env` file in the root directory and add your environment variables:
    ```
    MONDAY_API_TOKEN=your_monday_api_token
    SNUGGPRO_PUBLIC_KEY=your_snuggpro_public_key
    SNUGGPRO_PRIVATE_KEY=your_snuggpro_private_key
    BOARD_ID=your_board_id
    ```

## Usage

### Local Development

1. Start the Flask application on port 5000 (commonly open on local machines):
    ```bash
    python app/app.py
    ```
2. The application will be accessible at `http://localhost:5000`.
3. Configure Monday.com to send webhooks to your application endpoint, e.g., `http://localhost:5000/webhook`.

### Running with Docker

To run the application using Docker, follow these steps:

1. Build the Docker image:
    ```bash
    docker build -t snuggpro-automation .
    ```
2. Run the Docker container:
    ```bash
    docker run -p 5000:8080 --env-file .env snuggpro-automation
    ```
   - The Flask application inside the container listens on port `8080`, which is mapped to port `5000` on your local machine.

3. Your application should now be accessible at `http://localhost:5000`.

## Local Development with ngrok

`ngrok` allows you to expose your local server to the internet for webhook testing and other purposes. Here are the steps to set it up:

1. Download and install `ngrok` from [ngrok's website](https://ngrok.com/).
2. Run the Flask application on port 5000:
    ```bash
    python app/app.py
    ```
3. In a separate terminal window, expose the local port (5000) using `ngrok`:
    ```bash
    ngrok http 5000
    ```
4. Copy the provided `ngrok` URL (e.g., `https://abcd1234.ngrok.io`) and configure Monday.com to send webhooks to this URL.

## Deploying to Google Cloud Run

1. **Enable Cloud Run on your GCP project**:
    - Go to [Google Cloud Console](https://console.cloud.google.com/).
    - Enable the Cloud Run API.

2. **Authenticate the Google Cloud SDK**:
    ```bash
    gcloud auth login
    gcloud config set project your-project-id
    ```

3. **Build and submit the Docker image**:
    ```bash
    gcloud builds submit --tag gcr.io/your-project-id/snuggpro-automation
    ```

4. **Deploy to Cloud Run**:
    ```bash
    gcloud run deploy snuggpro-automation --image gcr.io/your-project-id/snuggpro-automation --platform managed --allow-unauthenticated --region us-central1
    ```
    - Adjust the `region` as needed.

5. **Set environment variables on GCP**:
    - Go to the [Cloud Run service](https://console.cloud.google.com/run).
    - Select your service.
    - Click "Edit & Deploy New Revision".
    - Add your environment variables under "Environment Variables".

## Updating Versions and Environment Variables on GCP

1. **To update the Docker image**:
    - Make changes to your application.
    - Build and push a new Docker image:
      ```bash
      gcloud builds submit --tag gcr.io/your-project-id/snuggpro-automation:version-2
      ```
    - Deploy the new image:
      ```bash
      gcloud run deploy snuggpro-automation --image gcr.io/your-project-id/snuggpro-automation:version-2 --platform managed
      ```

2. **To update environment variables**:
    - Go to the [Cloud Run service](https://console.cloud.google.com/run).
    - Select your service and click "Edit & Deploy New Revision".
    - Modify or add new environment variables as needed.
    - Click "Deploy".

## Testing

The project uses the `unittest` framework for testing. Test files are located in the `test/` directory.

To run all tests:
```bash
python -m unittest discover -s test
```

## Folder Structure

```
├── app/
│   ├── app.py            # Main Flask application
│   ├── config.py         # Configuration variables
│   ├── location.py       # Handles location-based logic
│   ├── mondayItem.py     # Interacts with Monday.com API
│   ├── snuggproJob.py    # Handles SnuggPro job creation
│   └── __init__.py
├── test/
│   ├── test_location.py  # Unit tests for location.py
│   ├── test_mondayItem.py# Unit tests for mondayItem.py
│   ├── test_snuggproJob.py# Unit tests for snuggproJob.py
│   └── __init__.py
├── Dockerfile            # Dockerfile to build the application image
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Contributing

1. Fork the repository
2. Create a new branch:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add feature"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-name
    ```
5. Create a pull request

## License

This project is licensed under the [MIT License](LICENSE).
