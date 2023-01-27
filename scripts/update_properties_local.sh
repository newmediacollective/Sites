#!/bin/bash
set -euo pipefail

form_args=()
for arg in "${@:2}"; do
    form_args+=(-F "$arg")
done

curl -i -H "Host: $1" "${form_args[@]}" http://localhost:5000/update_properties
