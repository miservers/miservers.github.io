
Install Jekyll

	https://jekyllrb.com/docs/installation



Install a Gem:

	gem install html-proofer -v 5.0.8

First Install Of miservers.github.io on Local:

	git clone https://github.com/miservers/miservers.github.io
	bundle update
	# bundle install

Run the Web server Jekyll:

	cd ~/miservers.github.io

	bundle exec jekyll serve 


	!!! Dont use nohup --> high cpu usage

Access Url:

	 http://127.0.0.1:4000/

---------------------------------
Systemd Unit                
---------------------------------
This is how to create a systemd unit to startup jekyll at the system boot.

- Create Script: **start_jekyll.sh**
	```sh
	#!/bin/bash

	WorkingDir=/home/jadmin/miservers.github.io

	# Vars
	export GEM_HOME="$HOME/gems"
	export PATH="$HOME/gems/bin:$PATH"
	export PATH="$HOME/.rbenv/bin:$PATH"
	eval "$(rbenv init -)"
	export GEM_HOME="$HOME/gems"
	export PATH="$HOME/gems/bin:$PATH"

	cd $WorkingDir

	bundle exec jekyll serve

	cd -
	```

- Create Systemd Unit: **/etc/systemd/system/miservices.service**
	```conf
	[Unit]
	Description=run jekyl for miservices.github.io

	[Service]
	Type=simple
	User=jadmin
	WorkingDirectory=/home/jadmin/miservers.github.io
	#ExecStart=/home/jadmin/gems/bin/bundle exec jekyll serve
	ExecStart=/home/jadmin/start_jekyll.sh
	# optional items below

	[Install]
	WantedBy=multi-user.target
	```

- Reload and Start the Service:
	```sh
	$ systemctl daemon-reload
	$ systemctl start  miservices.service
	```


