import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.lang.AutoCloseable;


public class PipeWriter implements AutoCloseable {
    private BufferedWriter pipe;

    public PipeWriter(String pipe_path) {
        try {
            this.pipe = new BufferedWriter(new FileWriter(pipe_path));
        } catch(IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    public void close() {
        try {
            this.pipe.close();
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    public void sendMessage(String msg) {
        try {
            this.pipe.write(msg + "\n");
            this.pipe.flush();
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }
}
