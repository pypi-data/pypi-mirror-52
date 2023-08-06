=================
 Syncurity Utils
=================

.. image:: https://badge.fury.io/py/syncurity-utils.svg
    :target: https://badge.fury.io/py/syncurity-utils
.. image:: https://circleci.com/gh/Syncurity/syncurity-utils/tree/master.svg?style=svg&circle-token=8a8847e25e6eed888591abb3fbc40ba165d2417e
    :target: https://circleci.com/gh/Syncurity/syncurity-utils/tree/master
.. image:: https://api.codacy.com/project/badge/Grade/878a6906207f44d99f0b746b4e30c55f
    :target: https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Syncurity/syncurity-utils&amp;utm_campaign=Badge_Grade
.. image:: https://api.codacy.com/project/badge/Coverage/878a6906207f44d99f0b746b4e30c55f
    :target: https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Syncurity/syncurity-utils&amp;utm_campaign=Badge_Coverage



The ``syncurity-utils`` package enables Automation and Orchestration efforts with the IR-Flow platform, in conjunction
with our other python packages.

Requirements

When using syncurity-utils in Stackstorm, you must install GCC.

On Centos7, run the following command to install GCC:

.. code-block:: bash

    $ sudo yum -y install gcc


Usage
~~~~~

Available on PyPI

.. code-block:: bash

    $ pip install syncurity-utils

Use in your Stackstorm pack like so:

.. code-block:: python

    from syncurity_utils import typecheck, find_domain
    from syncurity_utils.exceptions import TypecheckException


You can use the integration by doing the following:

.. code-block:: python

    from syncurity_utils.db.db import StackstormDB
    from syncurity_utils.db.alert import Alert
    import time

    db = StackstormDB("[user]", "[pass]", "[Database Name]", "[host]", [port])


At this point you can then get access to the helper methods for creating and querying alerts.

example:

.. code-block:: python

    db.add_alert(Alert(“{‘message’: ‘test message’}“, time.time(),‘Sensor_ref_name’, [IRFlow Alert Id], [Integration Id], [Tenant Id], [Alert Type Id]))
    db.delete_alert(1)
