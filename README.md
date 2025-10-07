# printer emulator (basic)

This README documents how to run, configure, and safely use the small web-based printer emulator included in `webserver.zip`, I haven't documented the code as it's pretty simple to follow the below and edit for your **LAB** requirements.

The script does have some Python requirements, but it is very basic and for simplicity I am not using virtual environments etc, it's running on a Windows 11 desktop with Python3 installed.

```Python
pip install -r requirements.txt
```
## I hate printers.  

Multi-function devices (MFDs), multi-function printers (MFPs), network scanners, I hate them all.

While preparing a presentation on **Service Account Fundamentals** (link) and creating a vulnerable Active Directory lab environment, I wanted to demonstrate something I’ve encountered repeatedly in real environments: **network-connected scanners and printers with LDAP lookup or scan to network functionality**.

The majority of printers, MFDs, and MFPs I’ve seen are configured with **default passwords** like `0000` or `123456` or `password`. These not only grant local control panel access but almost always also unlock the **web admin console**.

Years ago I read about using printer LDAP functionality to **obtain domain credentials**, so using ChatGPT’s, I decided to build a simple emulated device to figure out how easily credentials can be extracted from these systems.

A short while later, after some manual tweaks, I had a **basic web-based printer simulator** that you can launch with:

```Python
python3 webserver.py
```

The printer is preconfigured to use super-secure credentials:  `admin:password`

![](/images/printer01.png)

Clicking **Login** authenticates with the pre-populated credentials and redirects straight to the **LDAP configuration page**. The username and password fields are already populated; clicking **Connect** attempts to verify those credentials against the configured LDAP server IP.

![](/images/printer02.png)

Using WSL (or any Linux distro), you can host your own LDAP server and configure it to **support plaintext authentication (SSF=0)**:

```Bash
sudo apt install slapd ldap-utils

sudo dpkg-reconfigure -p low slapd

sudo nano olcSaslSecProps.ldif 

dn: cn=config
replace: olcSaslSecProps
olcSaslSecProps: noanonymous,minssf=0,passcred

sudo service slapd start    

sudo ldapmodify -Y EXTERNAL -H ldapi:// -f ./olcSaslSecProps.ldif && sudo service slapd restart

ldapsearch -H ldap:// -x -LLL -s base -b "" supportedSASLMechanisms

```

Once the LDAP server is configured, start a packet capture

```Bash
sudo tcpdump -SX -i eth0 tcp port 389
```

Back on the printer’s web console, set the **Server IP** to your LDAP server and click **Connect**.  

![](/images/printer03.png)

The authentication will fail(expected), but the packet capture will show the **LDAP bind request** containing the username and **plaintext password**.

![](/images/printer04.png)

Those captured credentials can then be used for **initial access**, or fed into tools such as `crackmapexec` to enumerate and move further through the environment.

## Code 

I've attached the webserver.zip file, with can be extra and ran as above, I haven't documented the code as it's pretty simple to follow through and edit for your **LAB** requirements.
