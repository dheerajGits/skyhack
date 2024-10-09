# Call Center Handle Time Prediction

## Overview

This project aims to optimize Average Handle Time (AHT) and Average Call Allocation Time in a call center environment using a predictive model. The project includes two Jupyter notebooks for data analysis and model training, as well as a Flask application to serve predictions.

Presentation Link:-

https://www.canva.com/design/DAGTGEKgBg8/-JRQiZCpv14VkxiuuBWV8w/edit?utm_content=DAGTGEKgBg8&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Endpoints](#endpoints)
- [Data Requirements](#data-requirements)
- [How to Run the Application](#how-to-run-the-application)
- [Example Requests](#example-requests)
- [License](#license)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_directory>

   ```

## Usage

### Project Structure

- `main_notebook.ipynb`: Contains data analysis and exploration of the datasets.
- `model_notebook.ipynb`: Contains the predictive model for calculating handle time.
- `app.py`: The main Flask application for serving predictions.

### Endpoints

1.  **Predict Endpoint**

        - **URL**: `/predict`
        - **Method**: `POST`
        - **Request Body**:

          json

          Copy code

          `{

    "customer_id": "12345",
    "primary_call_reason": "Flight Inquiry"
    }`

        - **Response**:

          json

          Copy code

          `{

    "transferred_to_agent": "agent_id_x",
    "least_handle_time": 300.5
    }`

2.  **Call Complete Endpoint**

        - **URL**: `/call_complete`
        - **Method**: `POST`
        - **Request Body**:

          json

          Copy code

          `{

    "agent_id": "agent_id_x"
    }`

        - **Response**:

          json

          Copy code

          `{

    "message": "Agent status updated to available."
    }`

## Data Requirements

``Ensure you have the following datasets in the `dataset` directory:

- `customer.csv`: Contains information about the customers.
- `calls.csv`: Contains details about the calls.
- `reason.csv`: Contains reasons for the calls.
- `sentiment_statistics.csv`: Contains sentiment analysis statistics.``

## How to Run the Application

1.  Navigate to the project directory:

    bash

    Copy code

    `cd <repository_directory>`

2.  Run the Flask application:

    bash

    Copy code

    `python app.py`

3.  The application will start on `http://127.0.0.1:5000`.

## Example Requests

### Predict Handle Time

bash

Copy code

`curl -X POST http://127.0.0.1:5000/predict \
-H "Content-Type: application/json" \
-d '{"customer_id": "12345", "primary_call_reason": "Flight Inquiry"}'`

### Update Agent Status

bash

Copy code

`curl -X POST http://127.0.0.1:5000/call_complete \
-H "Content-Type: application/json" \
-d '{"agent_id": "agent_id_x"}'`

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
