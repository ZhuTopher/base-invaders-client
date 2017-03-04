package main

import (
	"fmt"
    "log"
	"errors"
	"os"
	"net"

	"bufio"
)

// Return the Bloomburg game server's address
func GetServerAddr() (string, error) {
	addr := os.Getenv("BASE_IVDR_ADDR")
	if addr == "" {
		return "", errors.New("Missing/empty environment variable")
	}
	return addr, nil
}

// Return the Bloomburg game server's port
/*func GetServerPort() (string, error) {
	addr := os.Getenv("BASE_IVDR_PORT")
	if addr == "" {
		return "", errors.New("Missing/empty environment variable")
	}
	return addr, nil
}
*/
// Return our client's login credentials
func GetLoginCred() (string, string, error) {
	username := os.Getenv("USERNAME")
	pass := os.Getenv("PASSWORD")

	if (username == "" || pass == "") {
		return "", "", errors.New("Missing/empty environment variable")
	}
	
	return username, pass, nil
}

func main() {

	addr, err1 := GetServerAddr()
	if err1 != nil {
		log.Fatalf("Unable to fetch server addr. %v", err1)
	}
	/*port, err1 := GetServerAddr()
	if err1 != nil {
		log.Fatalf("Unable to fetch server addr. %v", err1)
	}*/

	user, pass, err2 := GetLoginCred()
	if err2 != nil {
		log.Fatalf("Unable to fetch server addr. %v", err2)
	}

   /* tcpl, err := net.ListenTCP("tcp",
    	&net.TCPAddr{IP: net.ParseIP(addr), Port: port})
	if err != nil {
		log.Fatalf("Unable to setup TCP connection to %s:%s. err: %v",
			addr, port, err)
		return err
	}*/

	// connect to this socket
    fmt.Printf("Attempting to connect to %s", addr)
	conn, netErr := net.Dial("tcp", addr)
	if netErr != nil {
		log.Fatalf("Unable to setup TCP connection to %s. err: %v",
			addr, netErr)
		return
	}
	defer conn.Close()

	// Send login credentials
	credentials := fmt.Sprintf("%s %s\n", user, pass)

  	fmt.Printf("Logging in as: %s", credentials)
  	fmt.Fprintf(conn, credentials)

    // Start Commands server
    commChan := make(chan string)
    go StartCommandsServer(&commChan)


    for {
        select {
        case cmd := <-commChan:
            if (cmd == "q") {
                commChan <- "q"
                break
            }

            // send to socket
            fmt.Fprintf(conn, cmd + "\n")
            // listen for reply
            message, _ := bufio.NewReader(conn).ReadString('\n')
            fmt.Printf("Message from server: %s\n", message)
            commChan <- message
        }
    }

    fmt.Println("Successfully closing BI Conn")

    // deferred conn.Close is called
}

func StartCommandsServer(commChan *chan string) {
    defer func(commChan *chan string){
        (*commChan) <- "q" // incidicate to close BI conn
    }(commChan)

    service := ":6060"
    tcpAddr, err := net.ResolveTCPAddr("tcp4", service)
    if err != nil {
        fmt.Printf("Failed to resolve tcp service: %v", err)
        return
    }

    listener, err := net.ListenTCP("tcp", tcpAddr)
    if err != nil {
        fmt.Printf("Failed to listen to tcp service: %v", err)
        return
    }

    conn, err := listener.Accept()
    if err != nil {
        fmt.Printf("Failed to accept command tcp client: %v", err)
        return
    }
    defer conn.Close()

    var buf [512]byte
    for {
        n, err := conn.Read(buf[0:])
        if err != nil {
            break
        }

        command := string(buf[0:n])
        fmt.Println(command)
        (*commChan) <- command
        result := <-(*commChan)
        _, err2 := conn.Write([]byte(result))
        if err2 != nil {
            break
        }
    }

    fmt.Println("Successfully closing Commands Conn")
}


/* 
package main

 import (
	"errors"
	"fmt"
	"fmt"
	"net"
	"os"
 )

 func handleUDPConnection(conn *net.UDPConn) {

         // here is where you want to do stuff like read or write to client

         buffer := make([]byte, 8192)

         n, addr, err := conn.ReadFromUDP(buffer)
         msg := string(buffer[:n])

         fmt.Println("UDP client : ", addr)
         fmt.Println("Received from UDP client :  ", msg)

         if err != nil {
                fmt.Fatal(err)
         }

         // NOTE : Need to specify client address in WriteToUDP() function
         //        otherwise, you will get this error message
         //        write udp : write: destination address required if you use Write() function instead of WriteToUDP()

         // write message back to client
         outPacket := []byte(fmt.Sprintf("Server received: %s", msg))
         _, err = conn.WriteToUDP(outPacket, addr)
         if err != nil {
                fmt.Println(err)
         }

 }

 // Return the deployed service application's PUBLIC_IP
func PublicIP() (string, error) {
	host := os.Getenv("PUBLIC_IP")
	if host == "" {
		return "", errors.New("Missing/empty public ip")
	}
	return host, nil
}

 func main() {
         hostName, err := PublicIP()
         if (err != nil) {
         	fmt.Fatalf("No ip to host server on: %v", err)
         }

         portNum := "6000"
         service := hostName + ":" + portNum

         udpAddr, err := net.ResolveUDPAddr("udp4", service)
         if err != nil {
                fmt.Fatal(err)
         }

         // setup listener for incoming UDP connection
         ln, err := net.ListenUDP("udp", udpAddr)
         if err != nil {
                fmt.Fatal(err)
         }
         defer ln.Close()
         fmt.Println("UDP server up and listening on " + udpAddr.String())

         // NOTE: server doesn't stop on EOF at the moment
         for {
                // wait for UDP client to connect
                handleUDPConnection(ln)
         }

        //go func(serviceAddr string){
        //}(service)
        //select{}
 }
 */
