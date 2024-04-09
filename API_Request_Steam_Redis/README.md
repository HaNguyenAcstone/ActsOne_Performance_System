**Description**

This Flask application demonstrates a scalable approach to handling high-volume requests with different processing requirements:

* **Just Get Request:** Handles 1 million transactions per second without message processing or response.
* **Not Save Message:** Processes 100,000 transactions per second, generates a simple message, but doesn't persist it.
* **Save Message:** Handles 10,000 transactions per second, retrieves data based on query parameters, saves messages to Redis Stream (`Redis_Streams_AcstOne`), and sends a confirmation response.

**Technology Stack**

* Flask: Lightweight Python web framework ([https://flask.palletsprojects.com/](https://flask.palletsprojects.com/))
* Redis: In-memory data store with stream capabilities ([https://redis.io/](https://redis.io/))
* RQ: Python library for managing asynchronous tasks ([https://python-rq.org/](https://python-rq.org/))

**Configuration**

* Redis Connection:
    * Host: `192.168.2.39` (replace with your Redis server address)
    * Port: `6379` (default Redis port)
    * Database: `0` (select a specific database if needed)
    * Stream Name: `Redis_Streams_AcstOne` (configure as needed)

**Running the Application**

1. Install dependencies:

   ```bash
   pip install Flask redis rq
   ```

2. Configure Redis connection details (if necessary) in the code.

3. Start the application:

   ```bash
   python app.py
   ```

   This will run the Flask development server on port 5000 (default) with debug mode enabled.

**API Endpoints**

* **GET /just_send_request**
   * Accepts 1 million requests per second without processing or response.
* **POST /not_save_message**
   * Handles 100,000 requests per second, generates a simple message ("Hello, I got your message"), but doesn't persist it.
* **GET /save_message**
   * Processes 10,000 requests per second:
     * Retrieves data from query parameters (`get` and `text`).
     * Creates multiple messages (based on `get`) containing the provided `text` and a sequential number.
     * Saves messages to the Redis Stream.
     * Returns confirmation message ("Hello, I saved your message").

**Additional Notes**

* Error handling is included to log exceptions and return appropriate error responses.
* Consider using a task queue worker (e.g., RQ Worker) to handle message processing asynchronously for the `/save_message` endpoint. This can further improve scalability.
* Explore logging and monitoring solutions for production deployments to track application health and performance.
* Adapt the configuration and API endpoints to match your specific requirements.
