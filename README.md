
# FastAPI CRUD Application

This project is a FastAPI application that allows you to perform CRUD (Create, Read, Update, Delete) operations for two entities: **Items** and **User Clock-In Records**. The application uses MongoDB for data storage and includes various filtering and aggregation features.

## Prerequisites

To get started, make sure you have the following:

- Python 3.7 or higher
- A MongoDB Atlas account or a local MongoDB instance
- Required Python packages

## Setup Instructions

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies

You’ll need to install the necessary Python packages. Use the following command:

```bash
pip install -r requirements.txt
```

### 3. Configure MongoDB

In your code, update the MongoDB connection string with your actual credentials:

```python
client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
```

### 4. Run the Application

You can run the application using the command below:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Make sure to replace `main` with the name of your Python file if it’s different.

### 5. Access Swagger UI

Once the application is running, you can view the interactive API documentation at:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

### Item APIs

- **Create Item**
  - `POST /items`
  - Example Input:
    ```json
    {
      "email": "user@example.com",
      "item_name": "Milk",
      "quantity": 10,
      "expiry_date": "2024-12-31"
    }
    ```
  - Response:
    ```json
    {
      "id": "<item_id>"
    }
    ```

- **Filter Items**
  - `GET /items/filter`
  - Query Parameters:
    - `email` (optional): Exact email match.
    - `expiry_date` (optional): Filter items expiring after the given date (YYYY-MM-DD).
    - `insert_date` (optional): Filter items inserted after the provided date (YYYY-MM-DD).
    - `quantity` (optional): Items with quantity greater than or equal to the given number.
  - Response: Aggregated count of items grouped by email.

- **Read Item by ID**
  - `GET /items/{item_id}`
  - Response: Details of the item.

- **Update Item**
  - `PUT /items/{item_id}`
  - Example Input: Same as the create item, excluding `insert_date`.
  - Response: Confirmation message.

- **Delete Item**
  - `DELETE /items/{item_id}`
  - Response: Confirmation message.

### Clock-In Record APIs

- **Create Clock-In Record**
  - `POST /clock-in`
  - Example Input:
    ```json
    {
      "email": "user@example.com",
      "location": "Office"
    }
    ```
  - Response:
    ```json
    {
      "id": "<record_id>"
    }
    ```

- **Filter Clock-In Records**
  - `GET /clock-in/filter`
  - Query Parameters:
    - `email` (optional): Exact email match.
    - `location` (optional): Exact location.
    - `insert_datetime` (optional): Clock-ins after the provided date (ISO format).
  - Response: List of clock-in records.

- **Read Clock-In Record by ID**
  - `GET /clock-in/{record_id}`
  - Response: Details of the clock-in record.

- **Update Clock-In Record**
  - `PUT /clock-in/{record_id}`
  - Example Input: Same as create clock-in, excluding `insert_datetime`.
  - Response: Confirmation message.

- **Delete Clock-In Record**
  - `DELETE /clock-in/{record_id}`
  - Response: Confirmation message.
