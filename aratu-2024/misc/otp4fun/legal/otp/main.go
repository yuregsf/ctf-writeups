package main

import (
	"net/http"
	"os"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/xlzd/gotp"
)

func main() {
	r := gin.Default()

	r.POST("/api/secrets", checkSecrets)

	r.LoadHTMLFiles("index.html")

	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", gin.H{})
	})

	r.Run(":8080")
}

type SecretRequest struct {
	Secrets []string `json:"secrets" binding:"required,len=6"`
}

func checkSecrets(c *gin.Context) {
	var req SecretRequest

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request. Provide exactly 6 secrets."})
		return
	}

	secretSet := make(map[string]struct{})
	for _, secret := range req.Secrets {
		if _, exists := secretSet[secret]; exists {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request. Provide different secrets."})
			return
		}
		secretSet[secret] = struct{}{}
	}

	for _, secret := range req.Secrets {
		if !getCurrentTOTP(secret) {
			c.JSON(http.StatusOK, gin.H{"result": "You loose!"})
			return
		}
	}
	flag := getFlag()

	c.JSON(http.StatusOK, gin.H{"result": "You win! Take your flag: " + flag})
}

func getFlag() string {
	file := "flag.txt"
	content, err := os.ReadFile(file)

	if err != nil {
		return ""
	}

	return string(content)
}

func getCurrentTOTP(secret string) bool {
	const targetOTP = 133737
	totp := gotp.NewDefaultTOTP(secret)
	now_code, err := strconv.Atoi(totp.Now())
	if err != nil {
		return false
	}

	if now_code == targetOTP {
		return true
	}
	return false
}
