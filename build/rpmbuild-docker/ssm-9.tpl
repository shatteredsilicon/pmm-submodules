 
config_opts['dnf.conf'] += """ 
[phantomjs] 
name = Repo for phantomjs 
baseurl = https://ftp.redsleeve.org/pub/misc/phantomjs/$basearch/ 
gpgcheck = 0 
enabled = 1 
""" 
