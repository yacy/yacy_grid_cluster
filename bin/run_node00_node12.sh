#! /bin/bash

ssh -o StrictHostKeyChecking=no pi@node01.local "$@" 2>&1 > >(sed 's/^/node01: /') &
pids01=$!
ssh -o StrictHostKeyChecking=no pi@node02.local "$@" 2>&1 > >(sed 's/^/node02: /') &
pids02=$!
ssh -o StrictHostKeyChecking=no pi@node03.local "$@" 2>&1 > >(sed 's/^/node03: /') &
pids03=$!
ssh -o StrictHostKeyChecking=no pi@node04.local "$@" 2>&1 > >(sed 's/^/node04: /') &
pids04=$!
ssh -o StrictHostKeyChecking=no pi@node05.local "$@" 2>&1 > >(sed 's/^/node05: /') &
pids05=$!
ssh -o StrictHostKeyChecking=no pi@node06.local "$@" 2>&1 > >(sed 's/^/node06: /') &
pids06=$!
ssh -o StrictHostKeyChecking=no pi@node07.local "$@" 2>&1 > >(sed 's/^/node07: /') &
pids07=$!
ssh -o StrictHostKeyChecking=no pi@node08.local "$@" 2>&1 > >(sed 's/^/node08: /') &
pids08=$!
ssh -o StrictHostKeyChecking=no pi@node09.local "$@" 2>&1 > >(sed 's/^/node09: /') &
pids09=$!
ssh -o StrictHostKeyChecking=no pi@node10.local "$@" 2>&1 > >(sed 's/^/node10: /') &
pids10=$!
ssh -o StrictHostKeyChecking=no pi@node11.local "$@" 2>&1 > >(sed 's/^/node11: /') &
pids11=$!
ssh -o StrictHostKeyChecking=no pi@node12.local "$@" 2>&1 > >(sed 's/^/node12: /') &
pids12=$!
ssh -o StrictHostKeyChecking=no pi@node00.local "$@" 2>&1 > >(sed 's/^/node00: /') &
pids00=$!

wait $pid00
wait $pid01
wait $pid02
wait $pid03
wait $pid04
wait $pid05
wait $pid06
wait $pid07
wait $pid08
wait $pid09
wait $pid10
wait $pid11
wait $pid12
echo finished "$@"
