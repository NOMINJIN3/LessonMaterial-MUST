/*
 * Small test client for the echo server.
 * Reads lines from standard input, sends each one to the server and prints
 * what the server echoes back.
 *
 *   echo "Hello there!" | java EchoClient [host [port]]
 */
import java.net.*;
import java.io.*;

public class EchoClient
{
    public static void main(String[] args)
    {
        String host = (args.length > 0) ? args[0] : "127.0.0.1";
        int port    = (args.length > 1) ? Integer.parseInt(args[1]) : 6007;

        try (Socket sock = new Socket(host, port)) {
            BufferedReader stdin =
                new BufferedReader(new InputStreamReader(System.in));
            InputStream  in  = sock.getInputStream();
            OutputStream out = sock.getOutputStream();

            String line;
            while ((line = stdin.readLine()) != null) {
                byte[] data = (line + "\n").getBytes("UTF-8");
                out.write(data);
                out.flush();

                /* the echo has exactly as many bytes as we sent */
                byte[] reply = new byte[data.length];
                int got = 0;
                while (got < reply.length) {
                    int n = in.read(reply, got, reply.length - got);
                    if (n == -1)
                        throw new EOFException("server closed the connection");
                    got += n;
                }
                System.out.print("echo: " + new String(reply, "UTF-8"));
            }
        }
        catch (IOException ioe) {
            System.err.println(ioe);
        }
    }
}
