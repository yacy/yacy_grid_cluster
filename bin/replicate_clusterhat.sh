#! /bin/bash

scp -o StrictHostKeyChecking=no $1 p1:$1
scp -o StrictHostKeyChecking=no $1 p2:$1
scp -o StrictHostKeyChecking=no $1 p3:$1
scp -o StrictHostKeyChecking=no $1 p4:$1

