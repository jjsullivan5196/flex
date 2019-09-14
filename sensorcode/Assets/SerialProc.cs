 using System.Collections;
using System.Collections.Generic;
using System.Threading;
using System.IO.Ports;
using System.Linq;
using System;

public class SerialProc
{
    SerialPort port;
    Thread sampler;

    float[] lastValue;
    float[] velocity;
    float[] sampleValue;
    const float smooth = 0.03f, cap = 0.8f, mul = 1.0f;
    string rawOut;

    public SerialProc()
    {
        port = new SerialPort("COM7", 57600);
        port.Open();
        port.ReadTimeout = 1000;

        sampleValue = new float[4];
        rawOut = "";

        sampler = new Thread(new ThreadStart(process));
        sampler.Start();
    }

    public float[] Sample
    {
        get { return (float[])sampleValue.Clone(); }
    }

    public string RawOut
    {
        get { return (string)rawOut.Clone(); }
    }

    void process()
    {
        bool firstRun = true;
        string[] rawVec;

        while (true)
        {
            rawOut = port.ReadLine();
            rawVec = rawOut.Split(',');
            port.BaseStream.Flush();

            if (rawVec.Length < 4)
                continue;

            float[] nvalues = Array.ConvertAll(rawVec, s => float.Parse(s) * mul);
            if (firstRun)
            {
                sampleValue = (float[])nvalues.Clone();
                firstRun = false;
            }
            
            for (int i = 0; i < 4; i++)
            {
                float diff = (nvalues[i] - sampleValue[i]) * smooth;
                if (diff > 0)
                    diff = Math.Min(diff, cap);
                else
                    diff = Math.Max(diff, -cap);
                sampleValue[i] += diff;
            }
        }
    }
}