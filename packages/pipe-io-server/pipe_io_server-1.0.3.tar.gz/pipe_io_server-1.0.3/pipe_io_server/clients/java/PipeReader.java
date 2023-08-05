import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.lang.AutoCloseable;


public class PipeReader implements AutoCloseable {
    private BufferedReader pipe;
    private MessageHandler messageHandler;

    public PipeReader(String pipe_path) {
        try {
            this.pipe = new BufferedReader(new FileReader(pipe_path));
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        this.messageHandler = new MessageHandler(){
            @Override
            public void call(String msg) {}
        };
    }

    public void close() {
        try {
            this.pipe.close();
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    public void setMessageHandler(MessageHandler handler) {
        this.messageHandler = handler;
    }

    public void run() {
        String msg;
        while ((msg = this.recvMessage()) != null) {
            this.messageHandler.call(msg);
        }
    }

    public String recvMessage() {
        try {
            return this.pipe.readLine();
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }
}
