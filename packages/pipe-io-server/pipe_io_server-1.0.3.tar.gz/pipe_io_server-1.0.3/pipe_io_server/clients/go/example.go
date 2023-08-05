package main

import (
	"log"
	"./pipeio"
)


func main() {
	pipeio, err := pipeio.NewPipeIO("in", "out")
	if err != nil {
		log.Fatal(err)
	}
	defer pipeio.Close()

	pipeio.Reader.SetMessageHandler(func(msg []byte) {
		pipeio.Writer.SendMessage(msg)
	})
	pipeio.Reader.Run()
}
