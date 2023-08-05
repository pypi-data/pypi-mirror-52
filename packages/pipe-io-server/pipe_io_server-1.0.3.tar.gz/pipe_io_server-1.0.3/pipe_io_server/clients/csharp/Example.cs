using System;
using Pipe.IO;

class Program
{
    static void Main(string[] args)
    {
        using (var t = new PipeIO("in", "out"))
        {
            t.Reader.OnMessage += (String msg) => t.Writer.SendMessage(msg);
            t.Reader.Run();
        }
    }
}
