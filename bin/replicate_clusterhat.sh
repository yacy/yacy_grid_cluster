#! /bin/bash

scp -o StrictHostKeyChecking=no $1 p1.local:$1
scp -o StrictHostKeyChecking=no $1 p2.local:$1
scp -o StrictHostKeyChecking=no $1 p3.local:$1
scp -o StrictHostKeyChecking=no $1 p4.local:$1

