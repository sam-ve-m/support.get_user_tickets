#!/bin/bash
fission spec init
fission env create --spec --name get-user-tickets-env --image nexus.sigame.com.br/python-env-3.8:0.0.4 --builder nexus.sigame.com.br/python-builder-3.8:0.0.1
fission fn create --spec --name get-user-tickets-fn --env get-user-tickets-env --src "./func/*" --entrypoint main.fn
fission route create --spec --method GET --url /get_user_tickets --function get-user-tickets-fn
