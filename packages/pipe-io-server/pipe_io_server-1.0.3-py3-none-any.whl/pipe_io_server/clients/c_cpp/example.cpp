#include <iostream>
#include <string>
#include <fstream>
#include "pipe_io.hpp"


int main() {
    PipeIO pipe_io("in", "out");
    pipe_io.reader.set_message_handler(
        [&pipe_io](std::string msg){pipe_io.writer.send_message(msg);}
    );
    pipe_io.reader.run();
}
