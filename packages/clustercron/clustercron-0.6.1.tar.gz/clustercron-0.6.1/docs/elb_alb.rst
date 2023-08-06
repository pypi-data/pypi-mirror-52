.. _clustercron-elb-alb:

Clustercron AWS LB
==================

Clustercron ELB
---------------

**Clustercron ELB**  will retrieve the *instance ID* of the instance (node
in a load balanced cluster) it is running on.

After retrieving the *health states* of all the nodes in the *load balancer
group*, clustercron checks if the node's *instance ID* is the first in the
(alphabetic) list of instances that have the state *InService*. If so it will
consider the node *master* and will run the given *command*.

If no *command* is given clustercron will exit 0 if the node is
considered *master* else clustercron will return 1.


Clustercron ALB
---------------

**Clustercron ALB** will retrieve the *instance ID* of the instance (node
in a target group) it is running on.

After retrieving the *health states* of all the nodes in the *target group*,
**Clustercron** checks if the node's *instance ID* is the first in the
(alphabetic) list of instances that have the state *healthy*. If so it will
consider the node *master* and will run the given *command*.

If no *command* is given clustercron will exit 0 if the node is
considered *master* else clustercron will return 1.


Cron job times and clustercron timeouts
---------------------------------------

Cron jobs wrapped with **Clustercron** should be started on the same time on
every node in the cluster. For syncronized time a **NTP** (or **Chrony**)
client is strongly advised.

Clusteron's timeout and retries settings should be minimized to syncronize
clustercron runs as much as possible. A time out of 2 seconds and a maximum of
1 retry is advised.


Boto 2
------

**Clustercron ELB** and **Clustercron ALB** both uses boto2_ for retreiving the
node's *instance ID* and optionally the node's *region* (if no *region* is
configured).

These actions don't need any boto2_ configuration or access management.


Boto 3
------

**Clustercron ELB** and **Clustercron ALB** both uses boto3_ for retreiving the
*health states* of all the nodes in the *load balancer group* (**ELB**) or the
*target group* (**ALB**).

*AWS policies* are needed for retreiving this information. The *AWS policies*
can be directly attached to *Users/Groups* or to *Roles* attached to the *AWS
EC2 instances*.

When a *AWS Policy* is directly attached to a user, credentials need to be
configured.


AWS Policy ELB
--------------

The user (or role) for checking the AWS **Load Balancer Groups** has to have
the following read rights::

  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "elasticloadbalancing:DescribeInstanceHealth",
                  "elasticloadbalancing:DescribeLoadBalancerAttributes",
                  "elasticloadbalancing:DescribeLoadBalancerPolicyTypes",
                  "elasticloadbalancing:DescribeLoadBalancerPolicies",
                  "elasticloadbalancing:DescribeLoadBalancers",
                  "elasticloadbalancing:DescribeTags"
              ],
              "Resource": "*"
          }
      ]
  }


AWS Policy ALB
--------------

The user (or role) for checking the AWS **Target Groups** has to have the
following read rights::

  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "elasticloadbalancing:DescribeTargetGroups",
                  "elasticloadbalancing:DescribeTargetHealth"
              ],
              "Resource": "*"
          }
      ]
  }


AWS credentials
---------------

When *AWS policies* are directly attached to a user, credentials  be
configured in the `~/.aws/credentials` file.

When *AWS policies* are attached to *AWS Roles* there is no need for this
configuration.


AWS config
----------

When no *region* is configured **Clustercfron ELB** and **Clustercron ALB**
will get the **AWS region** of the instance it is running on (using
*instance_metadata*). If a *region* is configured, it will use the configured
*region*.

Example configuration `~/.aws/config`::

  [default]
  region = eu-west-1


.. _boto2: http://boto.cloudhackers.com/en/latest/
.. _boto3: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
