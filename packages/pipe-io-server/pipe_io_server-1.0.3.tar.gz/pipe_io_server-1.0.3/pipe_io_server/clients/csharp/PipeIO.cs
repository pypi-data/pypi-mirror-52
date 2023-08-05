using System;
using System.IO;


namespace Pipe.IO
{
    public class PipeReader : IDisposable
    {
        public delegate void MessageHandler(String msg);
        public event MessageHandler OnMessage;
        private StreamReader pipe;

        public PipeReader(String pipe_path)
        {
            var fileStream = File.OpenRead(pipe_path);
            this.pipe = new StreamReader(fileStream);
        }

        public void Dispose()
        {
            this.pipe.Close();
        }

        public void Run()
        {
            String msg;
            while ((msg = this.RecvMessage()) != null)
            {
                if (this.OnMessage != null)
                {
                    this.OnMessage(msg);
                }
            }
        }

        public String RecvMessage()
        {
            return this.pipe.ReadLine();
        }
    }


    public class PipeWriter : IDisposable
    {
        private StreamWriter pipe;

        public PipeWriter(String pipe)
        {
            var fileStream = File.OpenWrite(pipe);
            this.pipe = new StreamWriter(fileStream);
        }

        public void Dispose()
        {
            this.pipe.Close();
        }

        public void SendMessage(String msg)
        {
            this.pipe.WriteLine(msg);
            this.pipe.Flush();
        }
    }


    public class PipeIO : IDisposable
    {
        public PipeReader Reader;
        public PipeWriter Writer;

        public PipeIO(String in_pipe_path, String out_pipe_path)
        {
            this.Reader = new PipeReader(in_pipe_path);
            this.Writer = new PipeWriter(out_pipe_path);
        }

        public void Dispose()
        {
            this.Reader.Dispose();
            this.Writer.Dispose();
        }
    }
}
