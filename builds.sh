set -o errexit
pip install -r requirements.txt
python manage.py migrate

sudo apt-get install pulseaudio
pulseaudio --start
export PULSE_SERVER=unix:/tmp/pulse-socket
