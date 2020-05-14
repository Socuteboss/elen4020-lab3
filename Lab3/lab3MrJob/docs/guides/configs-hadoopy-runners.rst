Hadoop-related options
======================

Since mrjob is geared toward Hadoop, there are a few Hadoop-specific options.
However, due to the difference between the different runners, the Hadoop
platform, and Elastic MapReduce, they are not all available for all runners.


Options specific to the local and inline runners
------------------------------------------------

.. mrjob-opt::
    :config: hadoop_version
    :switch: --hadoop-version
    :type: :ref:`string <data-type-string>`
    :set: local
    :default: ``None``

    Set the version of Hadoop to simulate (this currently only matters for
    :mrjob-opt:`jobconf`).

    If you don't set this, the ``local`` and
    ``inline`` runners will run in a version-agnostic mode, where anytime
    the runner sets a simulated jobconf variable, it'll use *every* possible
    name for it (e.g. ``user.name`` *and* ``mapreduce.job.user.name``).

.. mrjob-opt::
   :config: num_cores
   :switch: --num-cores
   :type: integer
   :set: local
   :default: ``None``

   Maximum number of tasks to handle at one time. If not set, defaults to the
   number of CPUs on your system.

   This also affects the number of input file splits the runner makes (the
   only impact in ``inline`` mode).

   .. versionadded:: 0.6.2


Options available to local, hadoop, and emr runners
---------------------------------------------------

These options are both used by Hadoop and simulated by the ``local``
and ``inline`` runners to some degree.

.. mrjob-opt::
    :config: jobconf
    :switch: -D, --jobconf
    :type: :ref:`jobconf dict <data-type-jobconf-dict>`
    :set: all
    :default: ``{}``

    ``-D`` args to pass to hadoop streaming. This should be a map from
    property name to value.  Equivalent to passing ``['-D',
    'KEY1=VALUE1', '-D', 'KEY2=VALUE2', ...]`` to
    :mrjob-opt:`hadoop_extra_args`

    .. versionchanged:: 0.6.6

       added the ``-D`` switch on the command line, to match Hadoop.

    .. versionchanged:: 0.6.6

       boolean ``true`` and ``false`` values in config files are
       passed correctly to Hadoop (see
       :ref:`JobConf dicts <data-type-jobconf-dict>`)


Options available to hadoop and emr runners
-------------------------------------------

.. mrjob-opt::
    :config: hadoop_extra_args
    :switch: --hadoop-args
    :type: :ref:`string list <data-type-string-list>`
    :set: all
    :default: ``[]``

    Extra arguments to pass to hadoop streaming.

.. mrjob-opt::
    :config: hadoop_streaming_jar
    :switch: --hadoop-streaming-jar
    :type: :ref:`string <data-type-string>`
    :set: all
    :default: (automatic)

    Path to a custom hadoop streaming jar.

    On EMR, this can be either a local path or a URI (``s3://...``). If you
    want to use a jar at a path on the master node, use a ``file://`` URI.

    On Hadoop, mrjob tries its best to find your hadoop streaming jar,
    searching these directories (recursively) for a ``.jar`` file with
    ``hadoop`` followed by ``streaming`` in its name:

    * ``$HADOOP_PREFIX``
    * ``$HADOOP_HOME``
    * ``$HADOOP_INSTALL``
    * ``$HADOOP_MAPRED_HOME``
    * the parent of the directory containing the Hadoop binary (see :mrjob-opt:`hadoop_bin`), unless it's one of ``/``, ``/usr`` or ``/usr/local``
    * ``$HADOOP_*_HOME`` (in alphabetical order by environment variable name)
    * ``/home/hadoop/contrib``
    * ``/usr/lib/hadoop-mapreduce``

    (The last two paths allow the Hadoop runner to work out-of-the box
    inside EMR.)

.. mrjob-opt::
   :config: libjars
   :switch: --libjars
   :type: :ref:`string list <data-type-string-list>`
   :set: all
   :default: ``[]``

   List of paths of JARs to be passed to Hadoop with the ``-libjars`` switch.

   ``~`` and environment variables within paths will be resolved based on the
   local environment.

   .. versionchanged:: 0.6.7

       Deprecated :option:`--libjar` in favor of :option:`--libjars`

   .. note::

      mrjob does not yet support *libjars* on Google Cloud Dataproc.

.. mrjob-opt::
    :config: label
    :switch: --label
    :type: :ref:`string <data-type-string>`
    :set: all
    :default: script's module name, or ``no_script``

    Alternate label for the job

.. mrjob-opt::
    :config: owner
    :switch: --owner
    :type: :ref:`string <data-type-string>`
    :set: all
    :default: :py:func:`getpass.getuser`, or ``no_user`` if that fails

    Who is running this job (if different from the current user)

.. mrjob-opt::
    :config: check_input_paths
    :switch: --check-input-paths, --no-check-input-paths
    :type: boolean
    :set: all
    :default: ``True``

    Option to skip the input path check. With ``--no-check-input-paths``,
    input paths to the runner will be passed straight through, without
    checking if they exist.

.. mrjob-opt::
    :config: spark_args
    :switch: --spark-args
    :type: :ref:`string list <data-type-string-list>`
    :set: all
    :default: ``[]``

    Extra arguments to pass to :command:`spark-submit`.

    .. warning::

       Don't use this to set ``--master``  or ``--deploy-mode``.
       On the Hadoop runner, you can change these with
       :mrjob-opt:`spark_master` and :mrjob-opt:`spark_deploy_mode`.
       Other runners don't allow you to set these because they can only
       handle the defaults.


Options available to hadoop runner only
---------------------------------------

.. mrjob-opt::
    :config: hadoop_bin
    :switch: --hadoop-bin
    :type: :ref:`command <data-type-command>`
    :set: hadoop
    :default: (automatic)

    Name/path of your :command:`hadoop` binary (may include arguments).

    mrjob tries its best to find :command:`hadoop`, checking all of the
    following places for an executable file named ``hadoop``:

    * ``$HADOOP_PREFIX/bin``
    * ``$HADOOP_HOME/bin``
    * ``$HADOOP_INSTALL/bin``
    * ``$HADOOP_INSTALL/hadoop/bin``
    * ``$PATH``
    * ``$HADOOP_*_HOME/bin`` (in alphabetical order by environment variable name)

    If all else fails, we just use ``hadoop`` and hope for the best.

    .. versionchanged:: 0.6.8

       Setting this to an empty value (``--hadoop-bin ''``) means to search
       for the Hadoop binary (used to effectively disable use of the
       :command:`hadoop` command).

.. mrjob-opt::
   :config: hadoop_log_dirs
   :switch: --hadoop-log-dir
   :type: :ref:`path list <data-type-path-list>`
   :set: hadoop
   :default: (automatic)

   Where to look for Hadoop logs (to find counters and probable cause of
   job failure). These can be (local) paths or URIs (``hdfs:///...``).

   If this is *not* set, mrjob will try its best to find the logs, searching in:

   * ``$HADOOP_LOG_DIR``
   * ``$YARN_LOG_DIR`` (on YARN only)
   * ``hdfs:///tmp/hadoop-yarn/staging`` (on YARN only)
   * ``<job output dir>/_logs`` (usually this is on HDFS)
   * ``$HADOOP_PREFIX/logs``
   * ``$HADOOP_HOME/logs``
   * ``$HADOOP_INSTALL/logs``
   * ``$HADOOP_MAPRED_HOME/logs``
   * ``<dir containing hadoop bin>/logs`` (see :mrjob-opt:`hadoop_bin`), unless the hadoop binary is in ``/bin``, ``/usr/bin``, or ``/usr/local/bin``
   * ``$HADOOP_*_HOME/logs`` (in alphabetical order by environment variable name)
   * ``/var/log/hadoop-yarn`` (on YARN only)
   * ``/mnt/var/log/hadoop-yarn`` (on YARN only)
   * ``/var/log/hadoop``
   * ``/mnt/var/log/hadoop``

.. mrjob-opt::
    :config: hadoop_tmp_dir
    :switch: --hadoop-tmp-dir
    :type: :ref:`path <data-type-path>`
    :set: hadoop
    :default: :file:`tmp/mrjob`

    Scratch space on HDFS. This path does not need to be fully qualified with
    ``hdfs://`` URIs because it's understood that it has to be on HDFS.

.. mrjob-opt::
    :config: spark_deploy_mode
    :switch: --spark-deploy-mode
    :type: :ref:`string <data-type-string>`
    :set: hadoop
    :default: ``'client'``

    Deploy mode (``client`` or ``cluster``) to pass to the ``--deploy-mode``
    argument of :command:`spark-submit`.

    .. versionadded:: 0.6.6

.. mrjob-opt::
    :config: spark_master
    :switch: --spark-master
    :type: :ref:`string <data-type-string>`
    :set: hadoop
    :default: ``'yarn'``

    Name or URL to pass to the ``--master`` argument of
    :command:`spark-submit` (e.g. ``spark://host:port``, ``yarn``).

    Note that archives (see :mrjob-opt:`upload_archives`) only work
    when this is set to ``yarn``.

.. mrjob-opt::
    :config: spark_submit_bin
    :switch: --spark-submit-bin
    :type: :ref:`command <data-type-command>`
    :set: hadoop
    :default: (automatic)

    Name/path of your :command:`spark-submit` binary (may include arguments).

    mrjob tries its best to find :command:`spark-submit`, checking all of the
    following places for an executable file named ``spark-submit``:

    * ``$SPARK_HOME/bin``
    * ``$PATH``
    * your :mod:`pyspark` installation's ``bin/`` directory
    * ``/usr/lib/spark/bin``
    * ``/usr/local/spark/bin``
    * ``/usr/local/lib/spark/bin``

    If all else fails, we just use ``spark-submit`` and hope for the best.

    .. versionchanged:: 0.6.8

       Searches for :command:`spark-submit` in :mod:`pyspark` installation.
