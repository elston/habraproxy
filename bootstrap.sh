# ....
set -e
prname="habraproxy"
# .......................................
sudo apt-get install -y python-pip
sudo pip install --upgrade pip
sudo pip install virtualenv
sudo pip install --upgrade virtualenv
sudo pip install virtualenvwrapper

touch /home/vagrant/.bashrc
echo " " >> /home/vagrant/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc

sudo -u vagrant bash -c "
    mkdir -p /vagrant/.envs
    ln -s /vagrant/.envs /home/vagrant/.virtualenvs
    export HOME=/home/vagrant/
    source /usr/local/bin/virtualenvwrapper.sh
    mkvirtualenv -p /usr/bin/python $prname
"

sudo -u vagrant bash -c "
    export HOME=/home/vagrant/
    source /home/vagrant/.virtualenvs/$prname/bin/activate     
    pip install -r /vagrant/requarements.txt    
"

sudo chmod +x /vagrant/habraproxy.py
exit 0