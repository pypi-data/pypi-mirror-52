import java.io.IOException;


public class PipeIO implements AutoCloseable {
    public PipeReader reader;
    public PipeWriter writer;

    public PipeIO(String in_pipe_path, String out_pipe_path) {
        this.reader = new PipeReader(in_pipe_path);
        this.writer = new PipeWriter(out_pipe_path);
    }

    public void close() {
        this.reader.close();
        this.writer.close();
    }
}
