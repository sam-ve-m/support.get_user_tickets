#!/bin/bash
fission spec init
fission env create --spec --name client-account-changes-env --image atilarmao/py-fission-env:v0.2 --builder atilarmao/py-fission-builder:v0.2
fission fn create --spec --name client-account-changes-fn --env client-account-changes-env --src "./*" --entrypoint func.main
fission route create --spec --method POST --url /post_client_account_changes_faas --function client-account-changes-fn