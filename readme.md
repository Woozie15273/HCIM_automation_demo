PHN Lookup Tool Documentation

This guide explains how the automated Personal Health Number (PHN) lookup tool works. It's designed to make things faster and easier.
________________________________________
📁 **Folder Structure**

/src
  /core
  
    - Config_loader: Converts settings from `.ini` to Python format
    
    - Context_manager: Creates a safe environment for running tasks
    
    - Logger: Records what happens during the run
    
    - Main_app: Controls the whole workflow
    
  /pages
    - Page Object Models (POM) used in the tool
    
  /utils
    - Extra tools that don’t fit in core or POM
    
/tests
  - Unit tests and smoke tests used during development

Config.ini: Main.py reads this to decide how to run. 

Main.py: Starting point of the tool.
________________________________________
🖥️ **Portable App**

You can turn this into a portable app using pyinstaller (--onefile).
This way, anyone can use it without a programming setup or a Super Admin account.
Minimum folder setup:
Main.exe       # Main program  
Config.ini     # Settings file
________________________________________
⚙️ **Configurations**

Edit config.ini with any text editor.

**Paths**

If left empty, the tool looks for the daily report in the same folder.

Recommended: Keep everything in one folder.

•	source_folder: Where you save the daily report

•	output_folder: Where PHN_Lookup and PHN_Results are created


**Files**

Uses name patterns to find reports, even if the name includes a date.


**Credentials**

•	If you're on VPN, it uses your current login.

•	If not, enter your credentials manually.


**Flags**

•	search_all_ha: True = search All_HA report; False = search MS report

•	on_ha_network: True = skip login; False = enter credentials

•	enable_log: Saves logs (usually not needed)

•	headless: True = browser is visible; False = browser is hidden


**URLs**

Helps the tool navigate using Selenium.


**Search**

Use Python-style list slicing:

•	[:] → Search all entries

•	[:50] → First 50 entries

•	[50:] → From entry 50 to the end

•	[50:100] → From entry 50 to 100
________________________________________
🔁 **Typical Workflow**

1.	Download both daily reports and put them in the same folder as main.exe.

2.	Adjust the settings in config.ini.

3.	Run main.exe. It will:

•	Read selected entries from the report

•	Open a browser and go to HCIM

•	Search each entry

•	Save results with score ≥ 10.0 to PHN_Results.xlsx
________________________________________
📊 **Handling Results**

•	If results are few, compare manually with the daily report.

•	If there are many (100+), use Excel’s =XLOOKUP() to match data in PHN_Lookup.

Lookup keys:

•	“Last Name”

•	“Date of Birth”

After using XLOOKUP:
1.	Copy the PHN column
2.	Paste as values
3.	Convert to number format
4.	Remove #N/A using CTRL+H
5.	Sort “HA RowId” column A-Z in both files
6.	Copy PHNs in bulk
________________________________________
🐞 **Known Issues**

•	Doesn’t fix data problems like reversed birth dates or names in all caps.


