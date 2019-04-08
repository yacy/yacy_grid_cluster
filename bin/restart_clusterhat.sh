#! /bin/bash

ssh -o StrictHostKeyChecking=no pi@p1 "sudo shutdown -r now"
ssh -o StrictHostKeyChecking=no pi@p2 "sudo shutdown -r now"
ssh -o StrictHostKeyChecking=no pi@p3 "sudo shutdown -r now"
ssh -o StrictHostKeyChecking=no pi@p4 "sudo shutdown -r now"
ssh -o StrictHostKeyChecking=no pi@controller "sudo shutdown -r now"
