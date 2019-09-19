#! /bin/bash

ssh -o StrictHostKeyChecking=no pi@node01 "$@" 2>&1 > >(sed 's/^/node01: /') &
pid01=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node02 "$@" 2>&1 > >(sed 's/^/node02: /') &
pid02=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node03 "$@" 2>&1 > >(sed 's/^/node03: /') &
pid03=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node04 "$@" 2>&1 > >(sed 's/^/node04: /') &
pid04=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node05 "$@" 2>&1 > >(sed 's/^/node05: /') &
pid05=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node06 "$@" 2>&1 > >(sed 's/^/node06: /') &
pid06=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node07 "$@" 2>&1 > >(sed 's/^/node07: /') &
pid07=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node08 "$@" 2>&1 > >(sed 's/^/node08: /') &
pid08=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node09 "$@" 2>&1 > >(sed 's/^/node09: /') &
pid09=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node10 "$@" 2>&1 > >(sed 's/^/node10: /') &
pid10=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node11 "$@" 2>&1 > >(sed 's/^/node11: /') &
pid11=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node12 "$@" 2>&1 > >(sed 's/^/node12: /') &
pid12=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node13 "$@" 2>&1 > >(sed 's/^/node13: /') &
pid13=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node14 "$@" 2>&1 > >(sed 's/^/node14: /') &
pid14=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node15 "$@" 2>&1 > >(sed 's/^/node15: /') &
pid15=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node16 "$@" 2>&1 > >(sed 's/^/node16: /') &
pid16=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node17 "$@" 2>&1 > >(sed 's/^/node17: /') &
pid17=$!
sleep 0.2
ssh -o StrictHostKeyChecking=no pi@node00 "$@" 2>&1 > >(sed 's/^/node00: /') &
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
wait $pid13
echo node13 ready
wait $pid14
echo node14 ready
wait $pid15
echo node15 ready
wait $pid16
echo node16 ready
wait $pid17
echo node17 ready
wait $pid00
echo node00 ready
echo finished "$@"
