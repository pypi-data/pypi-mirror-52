 #include "pipe_io.h"


void run2() {
    pipe_io pipeio = pipeio_new_io("in", "out");
    const char* line;
    while ((line = pipeio_recv_msg(&pipeio.reader))) {
        pipeio_send_msg(&pipeio.writer, line);
    }
    pipeio_close_io(&pipeio);
}

void msg_handler(const char* msg, void* ctx) {
    pipe_writer* writer = (pipe_writer*)(ctx);
    pipeio_send_msg(writer, msg);
}

void run1() {
    pipe_io pipeio = pipeio_new_io("in", "out");
    pipeio_set_msg_handler(&pipeio.reader, &msg_handler, &pipeio.writer);
    pipeio_run(&pipeio.reader);
    pipeio_close_io(&pipeio);
}

int main() {
    run1();  // or run2();
    // note that run1 and run2 do the same thing
    // and you can use whichever API you prefer
}
