### List project API

1. [Project Golang](#project-golang)
2. [Project Python](#project-python)
------
#### Project Golang

**Description**

This Go program simulates sending a large number of POST requests to a specified URL (`http://192.168.10.133:30002/send-message`) concurrently. It generates random order IDs and sends them as JSON data in the request body.

**Features**

* Sends multiple concurrent POST requests (configurable).
* Generates random order IDs for each request.
* Uses JSON to format request data.
* Handles potential errors during JSON marshalling and HTTP requests.

**Requirements**

* Go programming language (version 1.1 or later recommended)

**Installation**

1.  **Clone the repository** (if applicable).
2.  **Navigate to the project directory** in your terminal.
3.  **Build the Go program:**

    ```bash
    go build
    ```

**Usage**

1.  **Run the program:**

    ```bash
    ./your_program_name
    ```

    This will send the configured number of requests (default: 10,000 per run) to the target URL.

2.  **Modify configuration (optional):**

    - You can adjust the number of requests to send by changing the `numRuns` and `numMessages` constants in the code.
    - Update the target URL (`http://192.168.10.133:30002/send-message`) if it differs.

**Explanation**

The code defines three main functions:

* `main`:
    * Controls the overall execution loop.
    * Sets the number of runs (`numRuns`) and number of messages per run (`numMessages`).
    * For each run:
        * Creates a WaitGroup (`wg`) to synchronize concurrent requests.
        * Loops `numMessages` times to send individual requests concurrently.
        * Within the loop, uses a goroutine to:
            * Generate random order IDs.
            * Marshal the data into JSON format.
            * Send a POST request with the JSON data to the target URL.
            * Print a confirmation message upon successful sending.
        * Waits for all goroutines to finish using `wg.Wait()`.
        * Prints a message indicating the completion of the current run.
* `generatePostData`:
    * Seeds the random number generator.
    * Generates a random order ID string in a specific format.
    * Creates a map to hold the data (`key`: "ordersn", `value`: the generated order ID).
    * Returns the data map.
* `postRequest`:
    * Creates a new HTTP POST request using the provided URL and JSON data.
    * Sets the Content-Type header to "application/json".
    * Sends the request using an HTTP client.
    * Handles potential errors during request creation and execution.
    * Checks for non-200 status codes and returns an error if encountered.
    * Returns nil if the request was successful.

**Notes**

* This program focuses on sending requests concurrently. The target URL and its intended processing logic are assumed to be handled separately.
* Consider incorporating error handling within the target application (e.g., Flask API) to gracefully handle bulk requests like this.
* For larger-scale deployments, explore distributed task queuing solutions for improved performance and scalability.

-----

#### Project Python

**Import Statements:**

- `json`: Used to encode data into JSON format.
- `requests`: Essential for making HTTP requests to the target API endpoint.
- `concurrent.futures`: Provides the `ThreadPoolExecutor` class for executing tasks concurrently.
- `random`: Used for generating random data.
- `string`: Needed for accessing character sets for random string generation.

**`generate_random_value` Function:**

- **Purpose:** Creates a random string of a specified length.
- **Parameters:**
    - `length` (optional): The desired length of the random string. Defaults to 10.
- **Explanation:**
    - Combines letters and digits from `string.ascii_letters` and `string.digits` for a wider random character pool.
    - Uses `random.choice` to select characters and builds the string using list comprehension.
    - Returns the generated random string.

**`send_messages_to_api` Function:**

- **Purpose:** Sends a specified number of POST requests concurrently to the given API endpoint.
- **Parameters:**
    - `num_requests`: The number of requests to send.
- **Improvements:**
    - Clearer comments to explain each step.
    - Descriptive variable names (`data`, `futures`).
    - More efficient data creation within the loop to avoid unnecessary overhead.
    - Consistent use of `f-strings` for string formatting.

- **Code:**

```python
def send_messages_to_api(num_requests):
    url = "http://192.168.10.133:30002/send-message"
    headers = {'Content-Type': 'application/json'}

    with ThreadPoolExecutor() as executor:
        futures = []

        # Send POST requests concurrently
        for i in range(num_requests):
            data = {'key': 'test_key', 'value': generate_random_value()}
            future = executor.submit(send_message_to_api, url, data, headers)
            futures.append(future)

        # Wait for all requests to complete and print responses
        for future in futures:
            response = future.result()
            print(f"Response {i+1}: {response.text}")
```

**`send_message_to_api` Function:**

- **Purpose:** Sends a single POST request to the API using the provided URL, data, and headers.

- **Parameters:**
    - `url`: The API endpoint URL.
    - `data`: The JSON data to send in the request body.
    - `headers`: The HTTP headers for the request.
    
- **No changes required.**

**Explanation of Concurrency and Thread Pool Executor:**

- Sending multiple HTTP requests concurrently can improve performance by utilizing available resources more efficiently.
- The `concurrent.futures.ThreadPoolExecutor` provides a way to manage a pool of worker threads and execute tasks concurrently.
- In this code, the executor submits each request as a separate task, and multiple threads handle them simultaneously.

**How to Run the Code:**

1. Save the code as a Python file (e.g., `send_messages.py`).
2. Run the script from the command line:

   ```bash
   python send_messages.py
   ```

This will send 100,000 (default) POST requests concurrently to the specified API endpoint, printing the response text for each request.

**Additional Notes:**

- Adjust the `num_requests` variable in the `send_messages_to_api` function to change the number of requests sent.
- Ensure that the target API endpoint can handle concurrent requests efficiently.
- Consider error handling (e.g., exception handling) to gracefully handle potential request failures or API responses.