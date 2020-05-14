Cloud runner options
====================

These options are generally available whenever you run your job on a
Hadoop cloud service (:doc:`AWS Elastic MapReduce <emr-opts>`
or :doc:`Google Cloud Dataproc <dataproc-opts>`).

All options from :doc:`configs-all-runners` and :doc:`configs-hadoopy-runners`
are also available on cloud services.

Google credentials
------------------

See :ref:`google-setup` for specific instructions
about setting these options.


Choosing/creating a cluster to join
------------------------------------

.. mrjob-opt::
    :config: cluster_id
    :switch: --cluster-id
    :type: :ref:`string <data-type-string>`
    :set: cloud
    :default: automatically create a cluster and use it

    The ID of a persistent cluster to run jobs in (on Dataproc, this is the
    same thing as "cluster name").

    It's fine for other jobs to be using the cluster; we give our job's steps
    a unique ID.


Job placement
-------------

.. mrjob-opt::
    :config: region
    :switch: --region
    :type: :ref:`string <data-type-string>`
    :set: cloud
    :default: ``'us-west-2'`` on EMR, ``'us-west1'`` on Dataproc

    Geographic region to run jobs in (e.g.  ``us-central-1``).

    If mrjob create a temporary bucket, it will be created in this region as
    well.

    If you set region, you do not need to set :mrjob-opt:`zone`; a zone
    will be chosen for you automatically.

.. mrjob-opt::
   :config: subnet
   :switch: --subnet
   :type: :ref:`string <data-type-string>`
   :set: cloud
   :default: ``None``

   Optional subnet(s) to launch your job in.

   On Amazon EMR, this is the ID of a VPC subnet to launch cluster in
   (e.g. ``'subnet-12345678'``). This can also be a list of possible subnets
   if you are using :mrjob-opt:`instance_fleets`.

   On Google Cloud Dataproc, this is the name of a subnetwork (e.g.
   ``'default'``). Specifying *subnet* rather than :mrjob-opt:`network` will
   ensure that your cluster only has access to one specific geographic
   :mrjob-opt:`region`, rather than the entire VPC.

   .. versionchanged:: 0.6.8

      ``--subnet ''`` un-sets the subnet on EMR (used to be ignored).

   .. versionchanged:: 0.6.3

      Works on Google Cloud Dataproc as well as AWS Elastic MapReduce.

.. mrjob-opt::
    :config: zone
    :switch: --zone
    :type: :ref:`string <data-type-string>`
    :set: cloud
    :default: ``None``

    Zone within a specific geographic region to run your job in.

    If you set this, you do not neet to set :mrjob-opt:`region`.

Number and type of instances
----------------------------

.. mrjob-opt::
    :config: instance_type
    :switch: --instance-type
    :type: :ref:`string <data-type-string>`
    :set: cloud
    :default: ``m4.large`` or ``m5.xlarge`` on EMR, ``n1-standard-1`` on Dataproc

    Type of instance that runs your Hadoop tasks.

    Once you've tested a job and want to run it at scale, it's usually a good
    idea to use instances larger than the default. For EMR, see
    `Amazon EC2 Instance Types <https://aws.amazon.com/ec2/instance-types/>`__
    and for Dataproc, see
    `Machine Types <https://cloud.google.com/compute/docs/machine-types>`__.

    .. note::

       Many EC2 instance types can only run in a VPC (see
       :mrjob-opt:`subnet`).

    If you're running multiple nodes (see :mrjob-opt:`num_core_instances`),
    this option *doesn't* apply to the master node because it's just
    coordinating tasks, not running them. Use :mrjob-opt:`master_instance_type`
    instead.

    .. versionchanged:: 0.6.11

       Default on EMR is ``m5.xlarge`` on AMI version 5.13.0 and later, ``m4.large`` on earlier versions

    .. versionchanged:: 0.6.10

       Default on EMR changed to ``m5.xlarge``

    .. versionchanged:: 0.6.6

       Default on EMR changed to ``m4.large``. Was previously `m1.large`` if
       running Spark, ``m1.small`` if running on the (deprecated) 2.x AMIs,
       and ``m1.medium`` otherwise

.. mrjob-opt::
    :config: core_instance_type
    :switch: --core-instance-type
    :type: :ref:`string <data-type-string>`
    :set: cloud
    :default: value of :mrjob-opt:`instance_type`

    like :mrjob-opt:`instance_type`, but only for the core (worker) Hadoop
    nodes; these nodes run tasks and host HDFS. Usually you just want to use
    :mrjob-opt:`instance_type`.

.. mrjob-opt::
    :config: num_core_instances
    :switch: --num-core-instances
    :type: integer
    :set: cloud
    :default: 0 on EMR, 2 on Dataproc

    Number of core (worker) instances to start up. These run your job and
    host HDFS. This is in addition to the single master instance.

    On Google Cloud Dataproc, this must be at least 2.

.. mrjob-opt::
    :config: master_instance_type
    :switch: --master-instance-type
    :type: :ref:`string <data-type-string>`
    :set: cloud
    :default: (automatic)

    like :mrjob-opt:`instance_type`, but only for the master Hadoop node.
    This node hosts the task tracker/resource manager and HDFS, and runs tasks
    if there are no other nodes.

    If you're running a single node (no :mrjob-opt:`num_core_instances` or
    :mrjob-opt:`num_task_instances`), this will default to the value of
    :mrjob-opt:`instance_type`.

    Otherwise, on Dataproc, defaults to ``n1-standard-1``, and on EMR
    defaults to ``m1.medium`` (exception: ``m1.small`` on the
    deprecated 2.x AMIs), which is usually adequate for all but the largest
    jobs.

.. mrjob-opt::
    :config: task_instance_type
    :switch: --task-instance-type
    :type: :ref:`string <data-type-string>`
    :set: cloud
    :default: value of :mrjob-opt:`core_instance_type`

    like :mrjob-opt:`instance_type`, but only for the task
    (secondary worker) Hadoop nodes;
    these nodes run tasks but do not host HDFS. Usually you just want to use
    :mrjob-opt:`instance_type`.

.. mrjob-opt::
    :config: num_task_instances
    :switch: --num-task-instances
    :type: integer
    :set: cloud
    :default: 0

    Number of task (secondary worker) instances to start up. These run your
    job but do not host HDFS.

    You must have at least one core instance (see
    :mrjob-opt:`num_core_instances`) to run task instances; otherwise
    there's nowhere to host HDFS.

Cluster software configuration
------------------------------

.. mrjob-opt::
    :config: image_id
    :switch: --image-id
    :type: :ref:`string <data-type-string>`
    :set: cloud
    :default: None

    ID of a custom machine image.

    On EMR, this is complimentary with :mrjob-opt:`image_version`; you
    can install packages and libraries on your custom AMI, but it's up to
    EMR to install Hadoop, create the ``hadoop`` user, etc.
    :mrjob-opt:`image_version` may not be less than 5.7.0.

    You can use :py:func:`~mrjob.ami.describe_base_emr_images` to identify
    Amazon Linux images that are compatible with EMR.

    For more details about how to create a custom AMI that works with EMR, see
    `Best Practices and Considerations
    <https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-custom-ami.html#emr-custom-ami-considerations>`_.

    .. note::

       This is not yet implemented in the Dataproc runner.

    .. versionadded:: 0.6.5

.. mrjob-opt::
    :config: image_version
    :switch: --image-version
    :type: :ref:`string <data-type-string>`
    :set: cloud
    :default: ``'5.27.0'`` on EMR, ``'1.3'`` on Dataproc

    Machine image version to use. This controls which Hadoop
    version(s) are available and which version of Python is installed, among
    other things.

    See `the AMI version docs`_ (EMR) or `the Dataproc version docs`_ for
    more details.

    .. _`the AMI version docs`:
        http://docs.amazonwebservices.com/ElasticMapReduce/latest/DeveloperGuide/EnvironmentConfig_AMIVersion.html

    .. _`the Dataproc version docs`:
        https://cloud.google.com/dataproc/dataproc-versions

    You can use this instead of :mrjob-opt:`release_label` on EMR, even for
    4.x+ AMIs; mrjob will just prepend ``emr-`` to form the release label.

    .. versionchanged:: 0.6.12

       Default on Dataproc changed from ``1.0`` to ``1.3``

    .. versionchanged:: 0.6.11

       Default on EMR is now ``5.27.0``

    .. versionchanged:: 0.6.5

       Default on EMR is now ``5.16.0`` (was ``5.8.0``)

    .. warning::

       The 2.x series of AMIs is deprecated by Amazon and not recommended.

    .. warning::

        The 1.x series of AMIs is no longer supported because they use Python
        2.5.

.. mrjob-opt::
    :config: bootstrap
    :switch: --bootstrap
    :type: :ref:`string list <data-type-string-list>`
    :set: cloud
    :default: ``[]``

    A list of lines of shell script to run once on each node in your cluster,
    at bootstrap time.

    This option is complex and powerful. On EMR, the best way to get started
    is to read the :doc:`emr-bootstrap-cookbook`.

    Passing expressions like ``path#name`` will cause
    *path* to be automatically uploaded to the task's working directory
    with the filename *name*, marked as executable, and interpolated into the
    script by their absolute path on the machine running the script.

    *path*
    may also be a URI, and ``~`` and environment variables within *path*
    will be resolved based on the local environment. *name* is optional.
    For details of parsing, see :py:func:`~mrjob.setup.parse_setup_cmd`.

    Unlike with :mrjob-opt:`setup`, archives are not supported (unpack them
    yourself).

    Remember to put ``sudo`` before commands requiring root privileges!

.. mrjob-opt::
   :config: bootstrap_python
   :switch: --bootstrap-python, --no-bootstrap-python
   :type: boolean
   :set: cloud
   :default: ``True`` on Dataproc, as needed on EMR.

   Attempt to install a compatible (major) version of Python at bootstrap time,
   including header files and :command:`pip` (see :ref:`using-pip`).

   The only reason to set this to ``False`` is if you want to customize
   Python/pip installation using :mrjob-opt:`bootstrap`.

.. mrjob-opt::
    :config: extra_cluster_params
    :switch: --extra-cluster-param
    :type: :ref:`dict <data-type-plain-dict>`
    :set: cloud
    :default: ``{}``

    An escape hatch that allows you to pass extra parameters to the
    EMR/Dataproc API at cluster create time, to access API features that mrjob
    does not yet support.

    For EMR, see `the API documentation for RunJobFlow`_ for the full list of
    options.

    .. _`the API documentation for RunJobFlow`:
        http://docs.aws.amazon.com/ElasticMapReduce/latest/API/API_RunJobFlow.html

    Option names are strings, and values are data structures. On the command
    line, ``--extra-cluster-param name=value``:

    .. code-block:: sh

        --extra-cluster-param SupportedProducts='["mapr-m3"]'
        --extra-cluster-param AutoScalingRole=HankPym

    *value* can be either a JSON or a string (unless it starts with ``{``,
    ``[``, or ``"``, so that we don't convert malformed JSON to strings).
    Parameters can be suppressed by setting them to ``null``:

    .. code-block:: sh

        --extra-cluster-param LogUri=null

    This also works with Google dataproc:

    .. code-block:: sh

       --extra-cluster-param labels='{"name": "wrench"}'

    In the config file, `extra_cluster_param` is a dict:

    .. code-block:: yaml

        runners:
          emr:
            extra_cluster_params:
              AutoScalingRole: HankPym
              LogUri: null  # !clear works too
              SupportedProducts:
              - mapr-m3

    .. versionchanged:: 0.7.2

       Dictionaries will be recursively merged into existing
       parameters. For example:

       .. code-block:: yaml

          runners:
            emr:
              extra_cluster_params:
                Instances:
                  EmrManagedMasterSecurityGroup: sg-foo

    .. versionchanged:: 0.6.8

       You may use a *name* with dots in it to set (or unset) nested
       properties. For example:
       ``--extra-cluster-param Instances.EmrManagedMasterSecurityGroup=sg-foo``.

Monitoring your job
-------------------

.. mrjob-opt::
    :config: check_cluster_every
    :switch: --check-cluster-every
    :type: float
    :set: cloud
    :default: 10 seconds on Dataproc, 30 seconds on EMR

    How often to check on the status of your job, in seconds.

    .. versionchanged:: 0.6.5

       When the EMR client encounters a transient error, it will wait at
       least this many seconds before trying again.

.. mrjob-opt::
    :config: ssh_tunnel
    :switch: --ssh-tunnel, --no-ssh-tunnel
    :type: boolean
    :set: cloud
    :default: ``False``

    If True, create an ssh tunnel to the job tracker/resource manager and
    listen on a randomly chosen port.

    On EMR, this requires you to set
    :mrjob-opt:`ec2_key_pair` and :mrjob-opt:`ec2_key_pair_file`. See
    :ref:`ssh-tunneling` for detailed instructions.

    On Dataproc, you don't need to set a key, but you do need to have
    the :command:`gcloud` utility installed and set up (make
    sure you ran :command:`gcloud auth login` and
    :command:`gcloud config set project <project_id>`). See
    :ref:`installing-gcloud`.

    .. versionchanged:: 0.6.3

       Enabled on Google Cloud Dataproc

.. mrjob-opt::
    :config: ssh_tunnel_is_open
    :switch: --ssh-tunnel-is-open
    :type: boolean
    :set: cloud
    :default: ``False``

    if True, any host can connect to the job tracker through the SSH tunnel
    you open.  Mostly useful if your browser is running on a different machine
    from your job runner.

    Does nothing unless :mrjob-opt:`ssh_tunnel` is set.

.. mrjob-opt::
    :config: ssh_bind_ports
    :switch: --ssh-bind-ports
    :type: list of integers
    :set: cloud
    :default: ``range(40001, 40841)``

    A list of ports that are safe to listen on.

    The main reason to set this is if your firewall blocks the default range
    of ports, or if you want to pick a single port for consistency.

    On the command line, this looks like
    ``--ssh-bind-ports 2000[:2001][,2003,2005:2008,etc]``, where commas
    separate ranges and colons separate range endpoints.

Cloud Filesystem
----------------

.. mrjob-opt::
    :config: cloud_fs_sync_secs
    :switch: --cloud-fs-sync-secs
    :type: float
    :set: cloud
    :default: 5.0

    How long to wait for cloud filesystem (e.g. S3, GCS) to reach eventual
    consistency? This is typically less than a second, but the default is 5
    seconds to be safe.

.. mrjob-opt::
   :config: cloud_part_size_mb
   :switch: --cloud-part-size-mb
   :type: integer
   :set: cloud
   :default: 100

   Upload files to cloud filesystem in parts no bigger than this many megabytes
   (technically, `mebibytes`_). Default is 100 MiB.

   Set to 0 to disable multipart uploading entirely.

   Currently, Amazon `requires parts to be between 5 MiB and 5 GiB`_.
   mrjob does not enforce these limits.

   .. _`mebibytes`:
       http://en.wikipedia.org/wiki/Mebibyte
   .. _`recommended by Amazon`:
       http://docs.aws.amazon.com/AmazonS3/latest/dev/UploadingObjects.html
   .. _`requires parts to be between 5 MiB and 5 GiB`:
       http://docs.aws.amazon.com/AmazonS3/latest/dev/qfacts.html

   .. versionchanged:: 0.6.3

      Enabled on Google Cloud Storage. This used to be called
      *cloud_upload_part_size*.

.. mrjob-opt::
    :config: cloud_tmp_dir
    :switch: --cloud-tmp-dir
    :type: :ref:`string <data-type-string>`
    :set: cloud
    :default: (automatic)

    Directory on your cloud filesystem to use as temp space (e.g.
    ``s3://yourbucket/tmp/``, ``gs://yourbucket/tmp/``).

    By default, mrjob looks for a bucket belong to you whose name starts with
    ``mrjob-`` and which matches :mrjob-opt:`region`. If it can't find
    one, it creates one with a random name. This option is then set to `tmp/`
    in this bucket (e.g. ``s3://mrjob-01234567890abcdef/tmp/``).

Auto-termination
----------------

.. mrjob-opt::
    :config: max_mins_idle
    :switch: --max-mins-idle
    :type: float
    :set: cloud
    :default: 10.0

    Automatically terminate your cluster after it has been idle at least
    this many minutes. You cannot turn this off (clusters left idle
    rack up billing charges).

    If your cluster is only running a single job, mrjob will attempt to
    terminate it as soon as your job finishes. This acts as an additional
    safeguard, as well as affecting :ref:`cluster-pooling` on EMR.

    .. versionchanged:: 0.6.5

       EMR's idle termination script is more robust against
       :command:`sudo shutdown -h now` being ignored, and logs
       the script's stdout and stderr to
       ``/var/log/bootstrap-actions/mrjob-idle-termination.log``.

    .. versionchanged:: 0.6.3

       Uses Dataproc's built-in cluster termination feature rather than
       a custom script. The API will not allow you to set an idle time
       of less than 10 minutes.

    .. versionchanged:: 0.6.2

       No matter how small a value you set this to, there is a grace period
       of 10 minutes between when the idle termination daemon launches
       and when it may first terminate the cluster, to allow Hadoop to
       accept your first job.
