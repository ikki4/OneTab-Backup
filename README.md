# OneTab-Exporter

This is a Python script that will allow you to automatically* back up and manually restore your OneTab extension's tabs list.

*With Windows Task Scheduler

**Requires Python 3.4+ (I've only tested it on Python 3.8.11)**

**Note:** I'm a novice programmer and this script is in it's early stages of development, so expect some bugs/crashes. I'll do my best to fix every error I find, so keep checking this page to make sure you have the latest version. If you would like to fork my project and develop it even further, feel free to do so.

## What it does

It creates a text file containing your saved tabs' information (url and title), exactly as if you selected "Export/Import URLs" in Onetab and copied the "Export" section contents to a text file.

Then, if you ever need to restore a backup, just open the desired backup file, copy its contents and paste it in the "Import" section in Onetab. 

## What it does NOT

It does NOT save your tabs groups' name and status (starred, locked, etc). It saves the groups without the name and status.

## How to use

1. Clone this repository (or download the .py file).
2. Open `OneTab-Exporter.py` using a text editor or IDE.
   - In line 10 (variable CHROME_PATH), replace `<Username>` with your system user's username. For example, my path is `CHROME_PATH = r'C:\Users\ikki\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\chphlpgkkbolifaimnlloiipkdnihall'`.
   - If you wish to change the backups folder: In line 12 (variable EXPORT_PATH), replace that path with your backups folder path.
3. Then, you can run the script using `python OneTab-Exporter.py`.
4. If you want to automate the back ups (and use Windows), open up the Task Scheduler (search using the Windows key). Watch this [tutorial](https://www.youtube.com/watch?v=n2Cr_YRQk7o&feature=emb_title) or follow the steps below (thanks to [itsjoshthedeveloper](https://github.com/itsjoshthedeveloper) for [writing it](https://github.com/itsjoshthedeveloper/backupOneTab#how-to-use)):
   - In the left pane, click `Task Scheduler Library`.
   - In the right pane, click `Create Task...`
   - Name your Task.
   - Go to the `Actions` tab and click `New...` at the bottom.
   - Under Settings, for `Program/script` input your `python.exe` path. For example, my path is `C:\Users\ikki\anaconda3\python.exe`.
   - For `Add arguments` input `OneTab-Exporter.py`.
   - For `Start in` input the path of the directory where your `OneTab-Exporter.py` script is in. For example, my path is `D:\Downloads\OneTab-Exporter`.
   - Hit `OK`, go to the `Triggers` tab, and click `New...` at the bottom.
   - For `Begin the task` select `At log on`.
   - Under Settings, select `Specific user` make sure that is your username.
   - Hit `OK` twice, and it should work.
5. It's also possible to use `pyinstaller` to make an executable of the script to make it easier to run. Follow this [tutorial](https://datatofish.com/executable-pyinstaller/) to do that.

## How it works 

After trying out [other solutions](https://github.com/itsjoshthedeveloper/backupOneTab/issues/1), I found out that this folder: `C:\Users\<Username>\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\chphlpgkkbolifaimnlloiipkdnihall` contains a .log file that has multiple lines, each containing many Onetab backups. I noticed that the string with the latest backup is usually in the end of the .log file, and I also noticed that copying all the files in that folder and later restoring them was not enough for Onetab to restore the saved tabs.

So far, Onetab has not released an official way to parse through that file or to automatically backup the saved tabs, so I wrote my own. It's not perfect, since it does not store information like tab groups' names and their status (stared, locked, etc), but it mimics pretty well Onetab's manual Export feature.
