using System;
using System.Windows.Forms;

/*
 * Source: https://stackoverflow.com/a/25656379/3854436
 * Updates the time
 */
public class TimeUpdater
{
    public static void Main(string[] args)
    {
        TimeUpdater t = new TimeUpdater();
        string time = t.updateTime();
        Console.Out.WriteLine("OS time updated to: " + time);
        Console.In.ReadLine();
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

    string updateTime()
    {
        string time = DateTime.Now.ToString("h:mm:ss tt");
        SetTime(time);
        return time;
    }
}
