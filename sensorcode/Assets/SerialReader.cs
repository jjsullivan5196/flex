using System.Collections;
using System.Collections.Generic;
using System.IO;
using System;
using UnityEngine;

public class SerialReader : MonoBehaviour {

    SerialProc mSerial;
    List<string> rec;
    bool recording;
    float elapsed;

	// Use this for initialization
	void Start () {
        mSerial = new SerialProc();
        rec = new List<string>();
        recording = false;
        elapsed = 0.0f;
	}
	
	// Update is called once per frame
	void Update () {
        elapsed += Time.deltaTime;
        var mSample = mSerial.Sample;
        string tSample = string.Format("{0},{1},{2},{3},{4}", elapsed, mSample[0], mSample[1], mSample[2], mSample[3]);
        if (recording)
        {
            if (Input.GetKeyDown(KeyCode.K))
            {
                File.WriteAllLines(DateTime.Now.ToString("MM-dd-hh-mm-ss") + ".csv", rec.ToArray());
                rec.Clear();
                recording = !recording;
            }
            rec.Add(tSample);
            Debug.Log("REC: " + tSample);
        }
        else
        {
            if (Input.GetKeyDown(KeyCode.K))
            {
                recording = !recording;
            }
            Debug.Log(tSample);
            elapsed = 0.0f;
        }
	}
}
