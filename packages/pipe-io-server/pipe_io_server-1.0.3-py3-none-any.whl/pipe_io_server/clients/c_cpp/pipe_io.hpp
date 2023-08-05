extern "C" {
#include "pipe_io.h"
}
#include <string>
#include <iostream>
#include <functional>


class PipeReader {
public:
    PipeReader(const std::string& pipe_path)
    :preader(pipeio_new_reader(pipe_path.c_str())) {}

    virtual ~PipeReader() {
        pipeio_close_reader(&this->preader);
    }

    PipeReader(PipeReader&) = delete;
    PipeReader(PipeReader&&) = delete;
    PipeReader& operator=(const PipeReader&) = delete;
    PipeReader& operator=(const PipeReader&&) = delete;

    void set_message_handler(std::function<void(std::string)> message_handler) {
        this->message_handler = message_handler;
    }

    void run() {
        while (const char* linebuf = this->recv_message()) {
            std::string msg(linebuf);
            this->message_handler(msg);
        }
    }

    const char* recv_message() {
        return pipeio_recv_msg(&this->preader);
    }

private:
    pipe_reader preader;
    std::function<void(std::string)> message_handler = [](std::string){};
};


class PipeWriter {
public:
    PipeWriter(const std::string& pipe_path)
    :pwriter(pipeio_new_writer(pipe_path.c_str())) {}

    virtual ~PipeWriter() {
        pipeio_close_writer(&this->pwriter);
    }

    PipeWriter(PipeReader&) = delete;
    PipeWriter(PipeReader&&) = delete;
    PipeWriter& operator=(const PipeReader&) = delete;
    PipeWriter& operator=(const PipeReader&&) = delete;

    void send_message(std::string msg) {
        pipeio_send_msg(&this->pwriter, msg.c_str());
    }

private:
    pipe_writer pwriter;
};


class PipeIO {
public:
    PipeReader reader;
    PipeWriter writer;

    PipeIO(const std::string& in_pipe_path, const std::string& out_pipe_path)
    :reader(in_pipe_path), writer(out_pipe_path) {}

    PipeIO(PipeReader&) = delete;
    PipeIO(PipeReader&&) = delete;
    PipeIO& operator=(const PipeReader&) = delete;
    PipeIO& operator=(const PipeReader&&) = delete;
};
