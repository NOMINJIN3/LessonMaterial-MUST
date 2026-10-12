/*
 * Problem 3.25 - echo server.
 *
 * Waits for a client with accept().  For each connected client it loops:
 *     - read data from the socket into a buffer,
 *     - write the contents of the buffer back to the client.
 * The loop ends only when read() returns -1, i.e. when the client has closed
 * its end of the connection.
 *
 * The date server uses a BufferedReader (character stream); an echo server
 * must also cope with binary data, so it works on the byte streams
 * InputStream / OutputStream.
 *
 *   java EchoServer [port]        default port 6007
 */
import java.net.*;
import java.io.*;

public class EchoServer
{
    private static final int PORT = 6007;
    private static final int BUFFER_SIZE = 1024;

    public static void main(String[] args)
    {
        try {
            int port = (args.length > 0) ? Integer.parseInt(args[0]) : PORT;
            ServerSocket sock = new ServerSocket(port);
            System.out.println("Echo server listening on port " + port);

            while (true) {
                /* wait for a client connection */
                Socket client = sock.accept();
                System.out.println("client connected: "
                                   + client.getRemoteSocketAddress());
                try {
                    InputStream  in  = client.getInputStream();
                    OutputStream out = client.getOutputStream();

                    byte[] buffer = new byte[BUFFER_SIZE];
                    int n;
                    long total = 0;

                    /* read() returns -1 when the client closed the connection */
                    while ((n = in.read(buffer)) != -1) {
                        out.write(buffer, 0, n);       /* echo it back */
                        out.flush();
                        total += n;
                    }
                    System.out.println("client closed the connection, "
                                       + total + " bytes echoed");
                }
                catch (IOException ioe) {
                    System.err.println("client error: " + ioe);
                }
                finally {
                    client.close();
                }
            }
        }
        catch (IOException ioe) {
            System.err.println(ioe);
        }
    }
}
