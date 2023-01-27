#!/bin/bash
set -euo pipefail

form_args=()
for arg in "${@:2}"; do
    form_args+=(-F "$arg")
done

token=$(pyjwt --key=$(cat app/sites/$1/secret.txt) encode host=$1)
curl -i -H "Authorization: Bearer $token" "${form_args[@]}" https://$1/update_properties
