#! /bin/bash

ssh -o StrictHostKeyChecking=no pi@node01.local "$@" 2>&1 > >(sed 's/^/node01: /') &
pid01=$!
ssh -o StrictHostKeyChecking=no pi@node02.local "$@" 2>&1 > >(sed 's/^/node02: /') &
pid02=$!
ssh -o StrictHostKeyChecking=no pi@node03.local "$@" 2>&1 > >(sed 's/^/node03: /') &
pid03=$!
ssh -o StrictHostKeyChecking=no pi@node04.local "$@" 2>&1 > >(sed 's/^/node04: /') &
pid04=$!
ssh -o StrictHostKeyChecking=no pi@node05.local "$@" 2>&1 > >(sed 's/^/node05: /') &
pid05=$!
ssh -o StrictHostKeyChecking=no pi@node06.local "$@" 2>&1 > >(sed 's/^/node06: /') &
pid06=$!
ssh -o StrictHostKeyChecking=no pi@node07.local "$@" 2>&1 > >(sed 's/^/node07: /') &
pid07=$!
ssh -o StrictHostKeyChecking=no pi@node08.local "$@" 2>&1 > >(sed 's/^/node08: /') &
pid08=$!
ssh -o StrictHostKeyChecking=no pi@node09.local "$@" 2>&1 > >(sed 's/^/node09: /') &
pid09=$!
ssh -o StrictHostKeyChecking=no pi@node10.local "$@" 2>&1 > >(sed 's/^/node10: /') &
pid10=$!
ssh -o StrictHostKeyChecking=no pi@node11.local "$@" 2>&1 > >(sed 's/^/node11: /') &
pid11=$!
ssh -o StrictHostKeyChecking=no pi@node12.local "$@" 2>&1 > >(sed 's/^/node12: /') &
pid12=$!
ssh -o StrictHostKeyChecking=no pi@node00.local "$@" 2>&1 > >(sed 's/^/node00: /') &
pid00=$!

wait $pid01
echo node01 ready
wait $pid02
echo node02 ready
wait $pid03
echo node03 ready
wait $pid04
echo node04 ready
wait $pid05
echo node05 ready
wait $pid06
echo node06 ready
wait $pid07
echo node07 ready
wait $pid08
echo node08 ready
wait $pid09
echo node09 ready
wait $pid10
echo node10 ready
wait $pid11
echo node11 ready
wait $pid12
echo node12 ready
wait $pid00
echo node00 ready
echo finished "$@"
