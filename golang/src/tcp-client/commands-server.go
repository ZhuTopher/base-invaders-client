package main

/*

import "net"
import "fmt"
import "bufio"
import "strings" // only needed below for sample processing


func main() {

  fmt.Println("Launching server...")

  // listen on all interfaces
  ln, _ := net.Listen("tcp", ":6000")

  // accept connection on port
  conn, _ := ln.Accept()

  // run loop forever (or until ctrl-c)
  for {
    // will listen for message to process ending in newline (\n)
    message, _ := bufio.NewReader(conn).ReadString('\n')
    // output message received
    fmt.Print("Message Received:", string(message))
    // sample process for string received
    newmessage := strings.ToUpper(message)
    // send new string back to client
    conn.Write([]byte(newmessage + "\n"))
  }
}
*/


// Threaded Echo server
import (
    "net"
    "os"
    "fmt"
)

const DEFAULT_ERROR = "500"

type CmdsServer struct {
    biClient *BIClient
}

func NewCommandsServer(b *BICLient) (CmdsServer, error) {
    s := new(CmdsServer)
    s.biClient = b

    // create TCP listener
    service := ":1201"
    tcpAddr, err := net.ResolveTCPAddr("ip4", service)
    if err != nil {
        return nil, err
    }

    listener, err := net.ListenTCP("tcp", tcpAddr)
    if err != nil {
        return nil, err
    }

    go s.acceptLoop()

    return s, nil
}

func (s *CmdsServer) acceptLoop() {
    for {
        // accept a TCP client connection
        conn, err := listener.Accept()
        if err != nil {
            fmt.Print("Unable to accept CmdsServer conn.")
            continue
        }
        // run as a goroutine
        go handleClient(conn)
    }
}

func (s *CmdsServer) handleClient(conn net.Conn) {
    // close connection on exit
    defer conn.Close()

    var buf [512]byte
    for {
        // read upto 512 bytes (may need more)
        in, err := conn.Read(buf[0:])
        if err != nil {
            netErr := conn.Write([]byte{DEFAULT_ERROR})
            if netErr != nil {
                return // kill the client
            }
        } else {
            // write the n bytes read
            result, biErr := s.biClient.sendCommand(string{buf[0:in]})
            if biErr != nil {
                result = biErr.Error()
            }

            _, netErr := conn.Write([]byte{result})
            if netErr != nil {
                return // kill the client
            }
        }
    }
}
