#! /bin/bash

ssh -o StrictHostKeyChecking=no pi@p1.local "sudo shutdown -r now"
ssh -o StrictHostKeyChecking=no pi@p2.local "sudo shutdown -r now"
ssh -o StrictHostKeyChecking=no pi@p3.local "sudo shutdown -r now"
ssh -o StrictHostKeyChecking=no pi@p4.local "sudo shutdown -r now"
ssh -o StrictHostKeyChecking=no pi@controller.local "sudo shutdown -r now"
