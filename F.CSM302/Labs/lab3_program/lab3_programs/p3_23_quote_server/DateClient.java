/*
 * Date client of Figure 3.28, extended so that host and port can be given on
 * the command line (defaults: 127.0.0.1 and 6013, as in the book).
 * It can therefore read from the date server (6013), the quote server (6017)
 * and the haiku server (5575).
 *
 *   java DateClient [host [port]]
 */
import java.net.*;
import java.io.*;

public class DateClient
{
    public static void main(String[] args)
    {
        String host = (args.length > 0) ? args[0] : "127.0.0.1";
        int port    = (args.length > 1) ? Integer.parseInt(args[1]) : 6013;

        try {
            /* make connection to server socket */
            Socket sock = new Socket(host, port);

            InputStream in = sock.getInputStream();
            BufferedReader bin = new
                BufferedReader(new InputStreamReader(in));

            /* read the data from the socket */
            String line;
            while ( (line = bin.readLine()) != null)
                System.out.println(line);

            /* close the socket connection */
            sock.close();
        }
        catch (IOException ioe) {
            System.err.println(ioe);
        }
    }
}
