package main

import (
	"fmt"
    "log"
	"errors"
	"os"
	"net"

	"bufio"
)

const BI_QUIT = "q"

// TCP client to connect to Bloomburg's server
type BIClient struct {
    Addr string // host:port
    User string
    Pass string

    Conn net.Conn
    // cMutex sync.Mutex

    command chan string // channel holding commands
    done chan bool // channel to signal closing the connection
}

// Allocate a new BIClient
func NewBIClient(addr string, user string, pass string) (BIClient, error) {
    c = new(BIClient)
    c.Addr = addr
    c.User = user
    c.Pass = pass

    c.command = make(chan string, 10)
    c.done = make(chan bool)

    err = c.Connect()
    if err != nil {
        log.Fatalf("Unable to connect to BI server: %v", err)
        return nil, err
    }

    err = c.Login()
    if err != nil {
        log.Fatalf("Unable to connect to BI server: %v", err)
        return nil, err
    }

    return c, nil
}

func (c *BIClient) Connect() (err error) {
    // connect to this socket
    fmt.Printf("Attempting to connect to %s", addr)
    conn, err := net.Dial("tcp", addr)
    if err != nil {
        log.Fatalf("Unable to setup TCP connection to %s. err: %v",
            addr, err)
        return err
    }

    go func{
        select {
            case <-done: // blocks indefinitely waiting on done
                c.conn.Close()
        }

    }()

    return nil
}

// requires: c.Conn must be opened
func (c *BIClient) Login() (err error) {
    credentials := user + " " + pass + "\n"
    // credentials := fmt.Sprintf("%s %s\n", user, pass)

    // Send login credentials
    fmt.Printf("Logging in as: %s", credentials)
    fmt.Fprintf(conn, credentials)
     // listen for reply
    message, _ := bufio.NewReader(conn).ReadString('\n')
    fmt.Printf("Message from server: %s", message)

    return nil
}

func (c *BIClient) mainLoop() {
    for {
        select {
        case cmd := <-command:
            // if cmd is high priority, add to separate priority arrays

            if cmd == BI_QUIT {
                c.done.Close() // signal to close
                break
            } else {
                c.sendMessage(cmd)
            }
        }

        select {

        }
    }
}

func (c *BIClient) sendMessage() {
    
}