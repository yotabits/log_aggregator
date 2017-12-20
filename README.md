# log_to\_nuc #

* This tool allow to easily aggloremate logging files for support purpose.
* log\_to_nuc can send log files to nuc server or create a tarball of log files on local filesystem.
* log\_to_nuc can be configured thanks to ~/.log\_to\_nucrc file created automatically if it does not exist.
### Install ###
Simply add the path of the files/directories you want to add to the tarball to ~/.log\_to_nucrc configuration file.
 	
~~~~
git clone git@bitbucket.org:yujinrobot/log_pipeline.git

cd log_pipeline

sudo pip install log_to_nuc/
~~~~

### Configure ###
Simply add the path of the files/directories you want to add to the tarball to ~/.log\_to_nucrc configuration file.
 	
~~~~
/path/to/somefile1

~/relative/path/to/somefile2

~/relative/path/to/somedirectory
~~~~

### Usage ###
~~~~
  -h, --help      show this help message and exit
  --show_conf     Show the actual configuration file in use if it exists
  --default_conf  WARNING: Delete your actual conf if it exists and generate
                  the default configuration file
  --send          Send log files to the Nuc
  --local         Create a local tarball under home directory
~~~~

### TODO ###
* Write tests
* Think about name
* Integrate to yujintools