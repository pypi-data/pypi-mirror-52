PySVMON

PySVMON is a develoment project for SVMON client. It migrates bash-based client code to python. The development is based on python 2.7.13, and shall be tested on python 3.* version(TO DO).


Before installation, check your installation of pakiti-client, see whether it support --svmonreport option.
If unsupported, please remove it. A new version of pakiti-client will be installed with svmon client(rpm or pip).
Then one can use pip tools directly (root privileges if no virtualenv),

      pip install svmon-client

Update pip client to the latest version (pip 18.1 )

      pip install --upgrade pip

For test, just run the command svmon, the shell will return you help information. One can also try

     svmon -T (--test)

One can see an output with svmon client version.  This could cause error with old pip versions.


After test, the service owner could specify the parameters of its own service via command options, and save it
For example for svmon (currently not all service types are supported),

       svmon --site KIT --host svmon.eudat.eu --type svmon --dump

the --dump option will save the configuration to config.json file.   Currently, for B2HANDLE service, one need
to further input epic version file and handle server excutable directory into the client.


To check the current configuration, type

       svmon --show-config

To see output of svmon client,

       svmon --print

Make sure you have installed perl-libwww-perl, perl-LWP-Protocol-https packages.
Then try

       pakiti-client --svmonreport

to see the report collected by svmon client.
To send svmon report to our server, run pakiti client:

       pakiti-client --svmonreport --url https://svmon.eudat.eu:8443/api/serviceComponent/pakiti/report

One can add it to crontab. Or alternatively, direct post to the svmon server is supported, try:

       svmon --send

. However, you need install python requests library (http://docs.python-requests.org/en/master/user/install/#install).
In addition, to establish secure link, you will also need SSL trusted CA chain file.

Note: we also enclose the trusted CA file within the client: chain_TERENA_SSL_CA_3.pem.
