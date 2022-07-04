#!/bin/bash
fission spec init
fission env create --spec --name get-user-tickets-env --image nexus.sigame.com.br/python-env-3.8:0.0.5 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name get-user-tickets-fn --env get-user-tickets-env --src "./func/*" --entrypoint main.get_user_tickets
fission route create --spec --name et-user-tickets-rt --method GET --url /get_user_tickets --function get-user-tickets-fn
