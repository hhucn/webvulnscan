#!/bin/bash
MACHINE=$1
echo "Waiting for machine $MACHINE to poweroff..."

until $(VBoxManage showvminfo --machinereadable $MACHINE | grep -q ^VMState=.poweroff.)
do
  sleep 1
done
