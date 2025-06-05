<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/hkittelberger/RCStoSMS">
  </a>

<h3 align="center">RCS to SMS</h3>

  <p align="center">
    Convert RCS messages to SMS format for easy transfer to iOS.
    <br />
    <br />
    <br />
    <a href="https://github.com/hkittelberger/RCStoSMS">View Demo</a>
    &middot;
    <a href="https://github.com/hkittelberger/RCStoSMS/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/hkittelberger/RCStoSMS/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

When I was transfering over all my data from my Android to my new iPhone,
I realized the andorid app MovetoIOS does not handle RCS messages. This
script was created so I wouldn't have to lose any messages.

Unfortunately, there are still some limitations to this script. It will not 
handle any messages that aren't purely text so images, files, videos, etc.
will not be converted and skipped. The script does handle group messages, but
only to a certain extent. Due to how the text messages are downloaded from
android, their formatting of the numbers can be inconsistent. There are no
guarantees that the group messages will be converted correctly.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

You can convert your RCS messages to SMS format by running the script
convert.py from the repo on the command line. 

However, to get the text messages from your Android device, you will need to 
first download them using the Backup and Restore Andoid app from the Google 
Play Store. This app will allow you to create a backup of your messages in XML
format. Once you have created the backup, you can transfer the XML file to your
computer and run the script to convert the messages to SMS format. ALWAYS KEEP
A BACKUP OF YOUR XML FILES! 

You can view the text messages from the XML at this link:
[https://synctech.com.au/view-backup/](https://synctech.com.au/view-backup/)

After converting the messages, make sure your choose the new converted XML file
as your new backup location on the Backup and Restore Android app. Then, you 
can choose to restore the messages to your Android device. This will duplicate
all RCS / MMS messages as SMS messages, allowing you to transfer them to your
iPhone using the MovetoIOS app.

<!-- USAGE EXAMPLES -->
## Usage

Use the following command on the command line to run the script:

```sh
python3 convert.py <path_to_xml_file> [output_path]
```

<!-- CONTACT -->
## Contact

Holden Kittelberger - [LinkedIn](https://linkedin.com/in/holden-kittelberger) - holdenkittelberger@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>

