# snips-tv-skill
To interact with a TV through a SNIPS chatbot via a Broadlink BlackBean infra-red controller

Still very buggy :-)

References
https://github.com/TheGU/rm3_mini_controller
https://snips.gitbook.io/getting-started/ 


This library should be installed in /var/lib/snips/skills/snips-sonos-skill 
Run ./setup.sh to create the python virtual environment in venv

This repo contains a snapshot of rm3_mini_controller as of Nov 10th 2018, with an added, empty __init__.py file
<br>cd rm3_mini_controller
<br>pip install -r requirements.txt
<br>python test_run.py

The SNIPS skill is available at: https://console.snips.ai/app-editor/skill_b35ZoaXY898b

The code will be automaticall called through snips-skill-server. 
In order to run it manually and debug: 
sudo systemctl stop snips-skill-server 
source venv/bin/activate 
./action-tv.py

The program listens to SNIPS's message queue and handles commands to control the TV through the Blackbean IR controller.
