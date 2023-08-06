#!/bin/bash 
echo "==================================="
echo "Activate management plugin:"
echo "==================================="
rabbitmq-plugins enable rabbitmq_management

echo "==================================="
echo "Creating VHOSTs:"
echo "==================================="

rabbitmqctl add_vhost /lhcb
rabbitmqctl add_vhost /lhcb-jenkins
rabbitmqctl add_vhost /lhcb-test

rabbitmqctl list_vhosts

echo "==================================="
echo "Creating users:"
echo "==================================="
rabbitmqctl add_user lhcbadmin $1
rabbitmqctl add_user jenkins $1
rabbitmqctl add_user lhcb $1
rabbitmqctl add_user lhcbdev $1
rabbitmqctl add_user lhcbpr $1
rabbitmqctl delete_user guest

rabbitmqctl list_users

echo "==================================="
echo "Assigning users permissions:"
echo "==================================="

rabbitmqctl set_user_tags lhcbadmin administrator
rabbitmqctl set_permissions -p /lhcb lhcbadmin “.*” “.*” “.*”
rabbitmqctl set_permissions -p /lhcb lhcb “.*” “.*” “.*”
rabbitmqctl set_permissions -p /lhcb lhcbdev “.*” “.*” “.*”
rabbitmqctl set_permissions -p /lhcb lhcbpr “.*” “.*” “.*”
rabbitmqctl set_permissions -p /lhcb-jenkins lhcbadmin “.*” “.*” “.*”
rabbitmqctl set_permissions -p /lhcb-jenkins lhcb “.*” “.*” “.*”
rabbitmqctl set_permissions -p /lhcb-jenkins jenkins “.*” “.*” “.*”
rabbitmqctl set_permissions -p /lhcb-test lhcbadmin “.*” “.*” “.*”
rabbitmqctl set_permissions -p /lhcb-test lhcb “.*” “.*” “.*”
rabbitmqctl set_permissions -p /lhcb-test lhcbdev “.*” “.*” “.*”
rabbitmqctl set_permissions -p /lhcb-test lhcbpr “.*” “.*” “.*”
rabbitmqctl set_permissions -p / lhcbadmin “.*” “.*” “.*”
rabbitmqctl set_permissions -p / lhcb “.*” “.*” “.*”


echo "==================================="
echo "Ready"
echo "==================================="