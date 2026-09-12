#!/bin/bash
set -eu
cd -- "$(dirname -- "$0")"
install -Dm755 omarchy-bclm /usr/local/libexec/omarchy-bclm
install -Dm755 omarchy-charge /usr/local/libexec/omarchy-charge
install -Dm644 omarchy-charge.service /etc/systemd/system/omarchy-charge.service
systemctl daemon-reload
systemctl enable --now omarchy-charge.service
