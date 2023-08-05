# pipe-io-server
A trivial to use IPC solution based on POSIX named pipes and newlines.

## Why?
When it comes to communication between processes, we often find that
all we need is the simple abstraction of a text based message queue with
a blocking `send()` and `recv()` to connect 2 processes.

We could use sockets for instance, but that requires writing lots of
boilerplate. This can especially be a hassle if you want to support many
programming languages, as you would have to develop and maintain your
own bindings implementing your custom messaging protocol across all of them
(turning the abstraction of a byte stream into a queue of messages).

You could also use a message broker like RabbitMQ or Redis, but that would
force you to run a daemon in the background.
You could choose something like ZeroMQ, but all abstractions come with costs
(i.e how would you send a message to a ZMQ socket from a bash shell, or an
environment where ZMQ bindings are not easily available?).

What if you didn't have to maintain _any_ language bindings to
integrate with different languages?
What if you could rely on an API so trivial, that virtually every programming
language already provides it?

Some developers like doing IPC by writing and reading lines of text to and from named pipes.
It turns out that since a named pipe is like a file without `seek()`
(`stdin` or `stdout` _are_ pipes), you can use the readline and print utilities
of programming languages to use them.
Opening a pipe will block until the other side opens it and reading from it
also blocks until data is available. Just what we want!

The only issue is that writing a server for pipe based IO is not that
trivial if you wish to avoid blocking your main thread:
you have to start a thread for each pipe, avoid losing messages
when clients are opening and closing your pipes, deal with race conditions and so on.
It is especially hard to properly stop such a server: deadlocks are very easy to encounter
when juggling around with threads blocking on pipe operations.
This gets even more difficult if you wish your server to be resilient against irregular
client behaviour, such as the deletion of a named pipe while a thread is blocking on it.
This may sound discouraging, but this is the exact reason why I've written this package:
so you won't have to.
And solving all these issues are worth it in the end: writing clients is as trivial as it gets.

## What?
This package provides robust, asynchronous servers capable of IO over a text-based,
newline delimited protocol using named pipes.
This makes it extremely easy to integrate any external process as a plugin
into your application: clients can just open file descriptors for reading/writing
without worrying about anything else.

## Examples

A few lines of code are worth a 100 lines of API documentation.
You can find a simple usage example of this package in `echo_server.py`.

A client replying to each message of the server in just a few lines of bash
(`send` and `recv` are the paths of the pipes):
```
while IFS= read -r message; do
    printf "Received: ${message}\n"
    # ... do something ...
    printf "Some response\n" > "send"
done < "recv"
```

Some more examples:
- `pipe_io_server/clients` contains examples on how to use pipes in different languages
- `pipe_io_server/test_pipe_io_server.py` contains a relatively comprehensive suite of unit tests
