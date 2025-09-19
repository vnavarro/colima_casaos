# Jarbas

This script is a take on automating the setup and teardown of CasaOS inside Colima enviroment. 

The inspiration came from the many restarts had to be made when experimenting the configuration of CasaOS on home server / home lab machine and the need to save time and effort when doing so.

It is also a way to learn and keep fresh when working with tech.

## What it does?

When running jarbas.sh + jarbas.py the result is the following.

1 - check all necessary tools for Colima and CasaOS are installed:
* python3 (using [jarbas.sh](./jarbas.sh) first)
* docker
* Homebrew if deploying on MacOS
2 - check and install Colima if necessary
3 - creates the vm using Colima, if other than the default name and specs are desired check the args
4 - deploy and install CasaOS via ssh command

You may change the vm name (called profile by Colima), in that sense any Colima settings can be also configured via its defaults template.

Last but not least, for now, you can erase the vm with the destroy argument.

## How to use it?

First run jarbas.sh, it checks for python and install python3 if not installed already.

Then run jarbas.py, the full run can be done with:

`$ python3 jarbas.py -setup_casaos`

This will do everyting needed.

### What about other arguments?

Accepted args and its usage are as follows:

* -os: Set mac for macOS or linux for Linux (default: mac)
* -use_colima_defaults: Use colima default template file for configuration (default: False)
* -env_name: Name of the colima environment (default: casaosenv)
* -setup_casaos: Setup CasaOS inside the colima environment. Use this when colima is already installed.
* -destroy: Destroy the colima environment. When used with -env_name, it destroys the specified environment.

### License

GNU GENERAL PUBLIC LICENSE v3

[Check the COPYING file for full disclosure.](./COPYING)

Buy me a coffee and help out with bug squashing.

![donatecode](donatecode.png)

<html>
<form action="https://www.paypal.com/donate" method="post" target="_top">
<input type="hidden" name="business" value="M7ED48YE7PYXL" />
<input type="hidden" name="no_recurring" value="0" />
<input type="hidden" name="item_name" value="Me ajude a continuar esmagando bugs. Me pague um café?" />
<input type="hidden" name="currency_code" value="BRL" />
<input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
<img alt="" border="0" src="https://www.paypal.com/en_BR/i/scr/pixel.gif" width="1" height="1" />
</form>
</html>
