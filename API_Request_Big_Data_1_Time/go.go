package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"math/rand"
	"net/http"
	"sync"
	"time"
)

func main() {
	const numRuns = 1

	for run := 0; run < numRuns; run++ {
		var wg sync.WaitGroup
		const numMessages = 10000

		for i := 0; i < numMessages; i++ {
			wg.Add(1)
			go func(i int) {
				defer wg.Done()

				// Generate the POST data with a random ordersn and current timestamp
				postData := generatePostData()

				// Convert the struct to JSON
				jsonData, err := json.Marshal(postData)
				if err != nil {
					fmt.Println("Error encoding JSON:", err)
					return
				}

				// Send the POST request
				err = postRequest("http://192.168.10.133:30000/post_endpoint", jsonData)
				if err != nil {
					fmt.Println("Error sending request:", err)
					return
				}

				fmt.Printf("Message %d sent\n", i)
			}(i)
		}

		wg.Wait()
		fmt.Printf("Run %d completed\n", run+1)
	}
}

func generatePostData() map[string]string {
	rand.Seed(time.Now().UnixNano())
	ordersn := fmt.Sprintf("22%02d%02dQSK8S7BX", rand.Intn(100), rand.Intn(100))
	data := map[string]string{"key": "ordersn", "value": ordersn}
	return data
}

func postRequest(url string, jsonData []byte) error {
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("received non-200 status code: %d", resp.StatusCode)
	}
	return nil
}
