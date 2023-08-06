.. _configuration:

Configuration
=============

*Clustercron*'s operations are mostly handled by command line options.

See :ref:`usage` for more information.

There are some options that can be configured in *Clusetercron*'s configuration
file. For now only cache options are stated in the configuration.

*Clustercron* tries to read configuration from `/etc/clustercron.ini` and after
`.clustercron.ini` from the user's home directory. Options from the first will
be overridden by the latter (per option).


Default values for `clustercron.ini`::

    ; clustercron.ini
    [cache]
    filename = /tmp/clustercron_cache.json
    expire_time = 59
    max_iter = 20
