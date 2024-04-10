package main

import (
	"net/http"

	"github.com/Shopify/sarama"
	"github.com/gin-gonic/gin"
)

var (
	topicToUse   = "my-topic"
	kafkaBrokers = []string{"192.168.2.45:9092"}
)

func main() {
	// Khởi tạo router của Gin
	router := gin.Default()

	// Khởi tạo producer Kafka
	config := sarama.NewConfig()
	config.Producer.Return.Successes = true
	producer, err := sarama.NewSyncProducer(kafkaBrokers, config)
	if err != nil {
		panic(err)
	}
	defer producer.Close()

	// API POST
	router.POST("/send-message", func(c *gin.Context) {
		var data map[string]string
		if err := c.BindJSON(&data); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"success": false, "message": "Invalid JSON"})
			return
		}

		key := data["key"]
		if key == "" {
			key = "message"
		}
		value := data["value"]

		// Gửi message tới Kafka
		_, _, err := producer.SendMessage(&sarama.ProducerMessage{
			Topic: topicToUse,
			Key:   sarama.StringEncoder(key),
			Value: sarama.StringEncoder(value),
		})

		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"success": false, "message": err.Error()})
			return
		}

		c.JSON(http.StatusOK, gin.H{"success": true, "message": "Message sent successfully"})
	})

	// API GET
	router.GET("/get-message", func(c *gin.Context) {
		key := c.DefaultQuery("key", "message")
		value := c.DefaultQuery("value", "")

		// Gửi message tới Kafka
		_, _, err := producer.SendMessage(&sarama.ProducerMessage{
			Topic: topicToUse,
			Key:   sarama.StringEncoder(key),
			Value: sarama.StringEncoder(value),
		})

		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"success": false, "message": err.Error()})
			return
		}

		c.JSON(http.StatusOK, gin.H{"success": true, "message": "Message sent successfully"})
	})

	// Chạy ứng dụng trên cổng 5000
	router.Run(":5000")
}
