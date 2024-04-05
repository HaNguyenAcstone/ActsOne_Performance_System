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
			err = postRequest("http://192.168.2.39:30002/send-message", jsonData)
			if err != nil {
				fmt.Println("Error sending request:", err)
				return
			}

			fmt.Printf("Message %d sent\n", i)
		}(i)
	}

	wg.Wait()
	fmt.Println("All messages sent")
}

func generatePostData() map[string]string {
	rand.Seed(time.Now().UnixNano())
	ordersn := fmt.Sprintf("22%02d%02dQSK8S7BX", rand.Intn(100), rand.Intn(100))
	//	timestamp := time.Now().Unix()
	// return map[string]interface{}{
	// 	"items":              []interface{}{},
	// 	"ordersn":            ordersn,
	// 	"status":             "PROCESSED",
	// 	"completed_scenario": "",
	// 	"update_time":        timestamp,
	// }
	// return []map[string]interface{}{
	// 	{"key": "items", "value": []interface{}{}},
	// 	{"key": "ordersn", "value": ordersn},
	// 	{"key": "status", "value": "PROCESSED"},
	// 	{"key": "completed_scenario", "value": ""},
	// 	{"key": "update_time", "value": timestamp},
	// }
	data := map[string]string{"key": "ordersn", "value": ordersn}
	return data

	// return map[string]interface{}{
	// 	"topic": "ActsOnes_2",
	// 	"message": map[string]interface{}{
	// 		"data": map[string]interface{}{
	// 			"items":              []interface{}{},
	// 			"ordersn":            ordersn,
	// 			"status":             "PROCESSED",
	// 			"completed_scenario": "",
	// 			"update_time":        timestamp,
	// 		},
	// 		"shop_id":   727720655,
	// 		"code":      3,
	// 		"timestamp": timestamp,
	// 	},
	// }
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
