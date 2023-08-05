#pragma once
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>


typedef struct pipe_reader {
    FILE* stream;
    char* line_buf;
    size_t buf_size;
    void (*msg_handler)(const char*, void*);
    void* handler_ctx;
} pipe_reader;

static void null_handler(const char* msg, void* ctx) {}

pipe_reader pipeio_new_reader(const char* pipe_path) {
    pipe_reader preader;
    preader.stream = fopen(pipe_path, "r");
    preader.line_buf = NULL;
    preader.buf_size = 0;
    preader.msg_handler = &null_handler;
    return preader;
}

bool pipeio_check_reader(const pipe_reader* preader) {
    if (!preader || preader->stream == NULL) {
        return false;
    }
    return true;
}

const char* pipeio_recv_msg(pipe_reader* preader) {
    if (!pipeio_check_reader(preader)) {
        return NULL;
    }
    ssize_t read = getline(&preader->line_buf, &preader->buf_size, preader->stream);
    if (read > 0) {
        preader->line_buf[read - 1] = '\0';
        return preader->line_buf;
    }
    return NULL;
}

void pipeio_set_msg_handler(pipe_reader* preader, void (*msg_handler)(const char*, void*), void* handler_ctx) {
    if (msg_handler != NULL && handler_ctx != NULL) {
        preader->msg_handler = msg_handler;
        preader->handler_ctx = handler_ctx;
    }
}

void pipeio_run(pipe_reader* preader) {
    const char* line;
    while ((line = pipeio_recv_msg(preader))) {
        (*preader->msg_handler)(line, preader->handler_ctx);
    }
}

void pipeio_close_reader(pipe_reader* preader) {
    if (!pipeio_check_reader(preader)) {
        return;
    }
    fclose(preader->stream);
    preader->stream = NULL;
    if (preader->line_buf) {
        free(preader->line_buf);
        preader->line_buf = NULL;
    }
}


typedef struct pipe_writer {
    FILE* stream;
} pipe_writer;

pipe_writer pipeio_new_writer(const char* pipe_path) {
    pipe_writer pwriter;
    pwriter.stream = fopen(pipe_path, "w");
    return pwriter;
}

bool pipeio_check_writer(const pipe_writer* pwriter) {
    if (!pwriter || pwriter->stream == NULL) {
        return false;
    }
    return true;
}

bool pipeio_send_msg(pipe_writer* pwriter, const char* msg) {
    if (!pipeio_check_writer(pwriter)) {
        return false;
    }
    fprintf(pwriter->stream, "%s\n", msg);
    fflush(pwriter->stream);
    return true;
}

void pipeio_close_writer(pipe_writer* pwriter) {
    if (!pipeio_check_writer(pwriter)) {
        return;
    }
    fclose(pwriter->stream);
    pwriter->stream = NULL;
}


typedef struct pipe_io {
    pipe_reader reader;
    pipe_writer writer;
} pipe_io;

pipe_io pipeio_new_io(const char* in_pipe_path, const char* out_pipe_path) {
    pipe_io pipeio;
    pipeio.reader = pipeio_new_reader(in_pipe_path);
    pipeio.writer = pipeio_new_writer(out_pipe_path);
    return pipeio;
}

bool pipeio_check_io(const pipe_io* pipeio) {
    if (!pipeio) {
        return false;
    }
    return (pipeio_check_reader(&pipeio->reader) && pipeio_check_writer(&pipeio->writer));
}

void pipeio_close_io(pipe_io* pipeio) {
    if (!pipeio_check_io(pipeio)) {
        return;
    }
    pipeio_close_reader(&pipeio->reader);
    pipeio_close_writer(&pipeio->writer);
}

// const char* recv_msg_pipe_io(pipe_io* pipeio) {
//     if (!check_pipe_io(pipeio)) {
//         return NULL;
//     }
//     return recv_msg_pipe_reader(&pipeio->preader);
// }

// bool send_msg_pipe_io(pipe_io* pipeio, const char* msg) {
//     if (!check_pipe_io(pipeio)) {
//         return false;
//     }
//     return send_msg_pipe_writer(&pipeio->pwriter, msg);
// }
