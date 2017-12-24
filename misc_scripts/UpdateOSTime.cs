using System;
using System.Windows.Forms;
using System.Text.RegularExpressions;
using System.Net;
using System.Net.Cache;
using System.IO;

/*
 * Source: https://stackoverflow.com/a/9830462/3854436
 * Source2: https://stackoverflow.com/questions/2859790/the-request-was-aborted-could-not-create-ssl-tls-secure-channel
 */
public class InternetTime
{
    public static DateTime GetNistTime()
    {
        ServicePointManager.Expect100Continue = true;
        ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;

        DateTime dateTime = DateTime.MinValue;

        HttpWebRequest request = (HttpWebRequest)WebRequest.Create("http://nist.time.gov/actualtime.cgi?lzbc=siqm9b");
        request.Method = "GET";
        request.Accept = "text/html, application/xhtml+xml, */*";
        request.UserAgent = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)";
        request.ContentType = "application/x-www-form-urlencoded";
        request.CachePolicy = new RequestCachePolicy(RequestCacheLevel.NoCacheNoStore); //No caching
        HttpWebResponse response = (HttpWebResponse)request.GetResponse();
        if (response.StatusCode == HttpStatusCode.OK)
        {
            StreamReader stream = new StreamReader(response.GetResponseStream());
            string html = stream.ReadToEnd();//<timestamp time=\"1395772696469995\" delay=\"1395772696469995\"/>
            string time = Regex.Match(html, @"(?<=\btime="")[^""]*").Value;
            double milliseconds = Convert.ToInt64(time) / 1000.0;
            dateTime = new DateTime(1970, 1, 1).AddMilliseconds(milliseconds).ToLocalTime();
        } else
        {
            Console.Out.WriteLine(response.ResponseUri);
        }

        return dateTime;
    }
}

/*
 * Source: https://stackoverflow.com/a/25656379/3854436
 * Updates the time
 */
public class TimeUpdater
{
    public static void Main(string[] args)
    {
        TimeUpdater t = new TimeUpdater();
        string time = t.updateToInternetTime();
        Console.Out.WriteLine("OS time updated to: " + time);
		System.Threading.Thread.Sleep(2500);
        // Console.In.ReadLine();
    }

    public TimeUpdater()
    {
    }

    void SetDate(string dateInYourSystemFormat)
    {
        var proc = new System.Diagnostics.ProcessStartInfo();
        proc.UseShellExecute = true;
        proc.WorkingDirectory = @"C:\Windows\System32";
        proc.CreateNoWindow = true;
        proc.FileName = @"C:\Windows\System32\cmd.exe";
        proc.Verb = "runas";
        proc.Arguments = "/C date " + dateInYourSystemFormat;
        try
        {
            System.Diagnostics.Process.Start(proc);
        }
        catch
        {
            MessageBox.Show("Error to change time of your system");
            Application.ExitThread();
        }
    }

    void SetTime(string timeInYourSystemFormat)
    {
        var proc = new System.Diagnostics.ProcessStartInfo();
        proc.UseShellExecute = true;
        proc.WorkingDirectory = @"C:\Windows\System32";
        proc.CreateNoWindow = true;
        proc.FileName = @"C:\Windows\System32\cmd.exe";
        proc.Verb = "runas";
        proc.Arguments = "/C time " + timeInYourSystemFormat;
        try
        {
            System.Diagnostics.Process.Start(proc);
        }
        catch
        {
            MessageBox.Show("Error to change time of your system");
            Application.ExitThread();
        }
    }

    string updateToLocalTime()
    {
        string time = DateTime.Now.ToString("h:mm:ss tt");
        SetTime(time);
        return time;
    }

    string updateToInternetTime()
    {
        string time = InternetTime.GetNistTime().ToString("h:mm:ss tt");
        SetTime(time);
        return time;
    }
}
