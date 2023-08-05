public class Example {
    public static void main(String[] args) {
        try (PipeIO pipeio = new PipeIO("in", "out")) {
            pipeio.reader.setMessageHandler(new MessageHandler(){
                @Override
                public void call(String msg) {
                    pipeio.writer.sendMessage(msg);
                }
            });
            pipeio.reader.run();
        }
    }
}
