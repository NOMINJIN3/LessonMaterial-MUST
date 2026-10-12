/*
 * Problem 3.24 - haiku server.
 *
 * Listens to port 5575 (or the port given as first argument).  Each client
 * that connects receives one haiku - three lines of 5, 7 and 5 syllables -
 * and is then disconnected.  The date client (DateClient.java) can be used
 * to read the haiku:   java DateClient 127.0.0.1 5575
 */
import java.net.*;
import java.io.*;
import java.util.Random;

public class HaikuServer
{
    private static final int PORT = 5575;

    /* each haiku: 5 / 7 / 5 syllables */
    private static final String[] HAIKUS = {
        "Parent calls fork now\n"
            + "Child wakes up as a copy\n"
            + "Two paths, one story",

        "Child has come and gone\n"
            + "Parent sleeps and does not wait\n"
            + "A ghost in the list",

        "Bytes flow through the pipe\n"
            + "One writes and the other reads\n"
            + "Closed ends bring quiet",

        "Save the registers\n"
            + "Load another's state and run\n"
            + "Time slices go by",

        "Server waits at port\n"
            + "A client knocks, and the door\n"
            + "Opens to a stream",

        "Wind across the steppe\n"
            + "Horses run beneath blue sky\n"
            + "Silence holds the land"
    };

    public static void main(String[] args)
    {
        Random random = new Random();

        try {
            int port = (args.length > 0) ? Integer.parseInt(args[0]) : PORT;
            ServerSocket sock = new ServerSocket(port);
            System.out.println("Haiku server listening on port " + port);

            /* now listen for connections */
            while (true) {
                Socket client = sock.accept();

                PrintWriter pout = new
                    PrintWriter(client.getOutputStream(), true);

                /* write a randomly chosen haiku to the socket */
                pout.println(HAIKUS[random.nextInt(HAIKUS.length)]);

                /* close the socket and resume listening for connections */
                client.close();
            }
        }
        catch (IOException ioe) {
            System.err.println(ioe);
        }
    }
}
