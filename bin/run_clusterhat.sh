#! /bin/bash

ssh -o StrictHostKeyChecking=no pi@p1.local "$@" 2>&1 > >(sed 's/^/p1: /') &
pid01=$!
ssh -o StrictHostKeyChecking=no pi@p2.local "$@" 2>&1 > >(sed 's/^/p2: /') &
pid02=$!
ssh -o StrictHostKeyChecking=no pi@p3.local "$@" 2>&1 > >(sed 's/^/p3: /') &
pid03=$!
ssh -o StrictHostKeyChecking=no pi@p4.local "$@" 2>&1 > >(sed 's/^/p4: /') &
pid04=$!
ssh -o StrictHostKeyChecking=no pi@controller.local "$@" 2>&1 > >(sed 's/^/controller: /') &
pid05=$!

wait $pid01
echo p1 ready
wait $pid02
echo p2 ready
wait $pid03
echo p3 ready
wait $pid04
echo p4 ready
wait $pid05
echo controller ready
echo finished "$@"
