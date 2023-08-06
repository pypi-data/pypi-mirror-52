motioneyebot
============

A rudimentary Python program which utilizes a GroupMe bot to which can
make basic conversation with group members and provide functionality
to a MotionEyeOS camera on a network by communicating with the GroupMe
API through the requests library. The bot's responses represent the
personality -- and intelligence -- of my pet chicken, Popcorn, AKA Pops.

The CSV file which my weather_util module uses to get the coordinates
of a city can be found at https://simplemaps.com/data/us-cities and
is licensed under CC BY 4.0. All the text in the original file was
converted to lowercase for this project. View the license attribution
in "motioneyebot/data/csv_file_license.html".


Requires:
---------
- An internet connection.
- Python 3.5 or higher.

Setup:
------

**********************************************************
1) Create a GroupMe bot and add it to your selected group.
**********************************************************

You can create bots by registering an account on
https://dev.groupme.com/. This is also where you may find your
access token, bot ID, and group ID which you will be prompted
for the first time you launch the program. It is recommended
that you paste these items in a text editor buffer for later use.


******************************************************************
2) Install a web server on the machine that will run this program.
******************************************************************

Below demonstrates how to install Apache in Linux, though any
web server will suffice.

.. code:: bash

    sudo apt install -y apache2


*********************************************************************
3) Ensure ownership of directory containing your server's index file.
*********************************************************************

Below demonstrates giving user ownersip to Apache's html directroy
in Linux. This is the location where the program will download an
image from the motion camera and post to GroupMe on a user's request.
Keep note of this path as you will be asked to enter it the first time
you run the program.

.. code:: bash

    sudo chown -R [username]:[username] /var/www/html


*********************************************************************
4) Ensure a static IP address and forward TCP port 80 to the address.
*********************************************************************

You must ensure that the device which will run this program and
host your server has a static IP address. This process will vary
depending on the device you are using and the type of network/router
being used.

You must then forward the HTTP/TCP port 80 to the device's
static IP address. Port forwarding settings are available in most
routers' administrator settings. If you are already forwarding port
80 to another device, try using a port such as port 8000 or 8080.

You will also need to find your public ip address. This will be used
to allow GroupMe API to locate your HTTP server to download images
from. If you used a port besides 80, record your public IP address
in the form [IP]:[port] (i.e. 12.345.67.89:8000). This will be what
you enter in the 6th step of setup upon executing the program for
the first time.


*******************************************************
5) Configure the MotionEye camera's settings if needed.
*******************************************************

Locate the IP address of your MotionEyeOS camera. If you haven't
already, open the MotionEye system's settings and assign the camera's
IP address as static. You will be asked to enter this IP address in
the first time you run the program so you may want to record it as well.

OPTIONAL: If you have specified a Dropbox or Google Drive folder for
your MotionEye camera to upload content to, you may enter the URL in
the 'UPLOADS_URL' field. Otherwise, you may leave this section blank.


****************
6) Installation
****************

.. code:: bash

    pip3 install motioneyebot


*************
7) Execution
*************

The program should now be able to execute successfully. Note that
if your device has a power management feature that disconnects a
network interface (commonly WiFi), you will need to disable it to
allow the program to run continuously without having to reconnect
to the internet. The first time you execute the program, you will
walk through a setup process that looks like this:

::

    motioneyebot

    ################ motioneyebot Configuration ################

    Thank you for using motioneyebot! If you haven't already,

    take the time to read README.rst before continuing with setup.

            Press Enter to continue or 'q' to quit. >>

            1) Enter the your GroupMe access token >> f8ket0k3n
            2) Now enter your GroupMe bot ID >> f8k31d
            3) Now enter your GroupMe group ID >> f8kegr0up1d
            4) Enter the path to your server's index page >> /var/www/html
            5) Enter the IP address of your MotionEye camera >> 192.168.1.125
            6) Enter the public IP address of this device >> 12.345.67.89:8000
            *Optional* Enter the URL to your camera uploads >> https://drive.
            google.com/fakeurl
            *Optional* Enter the name for your Bot (only
            displays in this program) >> Pops
            *Optional* Enter the name for your Group (only
            displays in this program) >> Pops Alerts


After the initial setup, the program should start working automatically.
In the future, the program will look like the screen below after execution
wherein the box of text printed will repeat every 5 seconds as long as the
program was successfull in each attempt to fetch messages from the GroupMe
API.

.. code:: bash

    motioneyebot

    ####################
    # Bot: Pops
    # Group: Pops Alerts
    # Status: Listening
    ###################


*****************************
8) Editing the configuration.
*****************************

You can rerun the configuration script from the first launch of motioneyebot
any time by running the command below.

.. code:: bash

    motioneyeconfig


*************************************************
9) Messaging the Pops Bot in your GroupMe group:
*************************************************

PopCam Utilities
----------------

    - SNAP
      - Sends a recent snapshot from the PopCam.

    - STREAM
      - Sends URL to live stream (over LAN only).

    - UPLOADS
      - Sends URL to view all photos and videos captured.

Pops Weather Utility (US locations only)
----------------------------------------

    - “What’s the weather”
      - Sends weather at Pops’ coop.”

    - “What’s the forecast”

      - Sends 5-day forecast of weather at Pops’ coop.

    - “What’s the weather in [city]” / “What’s the weather in
      [city, state or state ID]”

      - Attempts to get weather data for the city specified and replies
        with weather or notifies that the location was not found.

      - "What’s the weather in [city, state or state ID]” is a better format.
        (If Morristown, New Jersey were first in the list and you asked
        for weather in Morristown expecting Morristown, TN, you would get
        the weather for Morristown, NJ instead.

    - “What’s the forecast in [city]” / “What’s the forecast in
      [city, state or state ID]”

      - Attempts to get 5-day weather forecast data for the city specified
        and replies with forecast or notifies that the location was not found.

      - Again, specifying [city, state or state ID] will be more accurate.

Talk to Popcorn. A few things to try:
-------------------------------------
- ”@pops What is the meaning of life?”
- ”@pops How are you?”
- ”@pops What’s up”
- ”@pops What are you doing?”
- ”@pops Where are you?”
- ”@pops How’s the weather?”
- ”@pops Tell me about your business”
- ”@pops Where are you from?”
- ”@pops Should I ___ or ___?”
- ”@pops Tell me a joke”
- ”@pops Tell me a proverb.”
- ”@pops Give me wisdom.”
