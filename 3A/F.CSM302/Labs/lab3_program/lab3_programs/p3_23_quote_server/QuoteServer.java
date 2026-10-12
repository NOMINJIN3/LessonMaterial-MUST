/*
 * Problem 3.23 - quote-of-the-day server (a modified date server, Figure 3.27).
 *
 * The well-known port 17 is reserved, so the server listens to port 6017
 * (or to the port given as the first command-line argument).
 * A quote is printable ASCII, has fewer than 512 characters and may span
 * several lines.  The quote changes from day to day.
 *
 *   javac QuoteServer.java DateClient.java
 *   java QuoteServer            (terminal 1)
 *   java DateClient 127.0.0.1 6017   (terminal 2)
 */
import java.net.*;
import java.io.*;
import java.time.LocalDate;

public class QuoteServer
{
    private static final int PORT = 6017;

    private static final String[] QUOTES = {
        "Simplicity is prerequisite for reliability.\n"
            + "  -- Edsger W. Dijkstra",
        "Testing shows the presence, not the absence of bugs.\n"
            + "  -- Edsger W. Dijkstra",
        "Programs must be written for people to read, and only\n"
            + "incidentally for machines to execute.\n"
            + "  -- Harold Abelson and Gerald Jay Sussman",
        "Talk is cheap. Show me the code.\n"
            + "  -- Linus Torvalds",
        "The best way to predict the future is to invent it.\n"
            + "  -- Alan Kay",
        "Premature optimization is the root of all evil.\n"
            + "  -- Donald E. Knuth",
        "Everyone knows that debugging is twice as hard as writing\n"
            + "a program in the first place.\n"
            + "  -- Brian W. Kernighan"
    };

    /** printable ASCII (newline allowed) and fewer than 512 characters */
    private static boolean isValid(String quote)
    {
        if (quote.length() >= 512)
            return false;
        for (int i = 0; i < quote.length(); i++) {
            char c = quote.charAt(i);
            if (c != '\n' && (c < 0x20 || c > 0x7E))
                return false;
        }
        return true;
    }

    /** the same quote is returned during the whole day */
    private static String quoteOfTheDay()
    {
        int day = LocalDate.now().getDayOfYear();
        return QUOTES[day % QUOTES.length];
    }

    public static void main(String[] args)
    {
        for (String q : QUOTES) {
            if (!isValid(q)) {
                System.err.println("invalid quote: " + q);
                return;
            }
        }

        try {
            int port = (args.length > 0) ? Integer.parseInt(args[0]) : PORT;
            ServerSocket sock = new ServerSocket(port);
            System.out.println("Quote server listening on port " + port);

            /* now listen for connections */
            while (true) {
                Socket client = sock.accept();

                PrintWriter pout = new
                    PrintWriter(client.getOutputStream(), true);

                /* write the quote to the socket */
                pout.println(quoteOfTheDay());

                /* close the socket and resume listening for connections */
                client.close();
            }
        }
        catch (IOException ioe) {
            System.err.println(ioe);
        }
    }
}
