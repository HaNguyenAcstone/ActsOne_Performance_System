package main

import (
	"fmt"
	"math/rand"
	"net/http"
	"runtime"
	"sync"
	"time"
)

func main() {
	const numRuns = 50

	for run := 0; run < numRuns; run++ {
		runtime.GC() // Clear memory after each run
		var wg sync.WaitGroup
		const numMessages = 1000

		for i := 0; i < numMessages; i++ {
			wg.Add(1)
			go func(i int) {
				defer wg.Done()

				// Generate the query parameters with a random ordersn
				//key := "ordersn"
				//value := 1

				// Construct the URL with the query parameters - Redis
				//url := fmt.Sprintf("http://192.168.2.39:30010/send-big-message?key=order&value=1")
				url := fmt.Sprintf("http://192.168.2.39:30005/push_orders?key=order&value=1")

				// Send the GET request
				err := getRequest(url)
				if err != nil {
					fmt.Println("Error sending request:", err)
					return
				}

				fmt.Printf("Message %d sent\n", i)
			}(i)
		}

		wg.Wait()
		runtime.GC() // Clear memory after each run
		fmt.Printf("Run %d completed\n", run+1)
	}
}

func generateOrdersn() string {
	rand.Seed(time.Now().UnixNano())
	ordersn := fmt.Sprintf("22%02d%02dQSK8S7BX", rand.Intn(100), rand.Intn(100))
	return ordersn
}

func getRequest(url string) error {
	resp, err := http.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("received non-200 status code: %d", resp.StatusCode)
	}

	return nil
}
