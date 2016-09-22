#!/bin/bash

rm -rf $1
mkdir -p $1/config
cat <<EOF > $1/config/$1.yaml
# config_version=3

mode:
  priority: 100
# code: $1.$1
  start_events: $1_selected
  stop_events: $1_complete, $1_failed

logic_blocks:
  sequences:
    $1:
      events:
        - s_test_3_active
      events_when_complete: $1_complete, carousel_mode_complete
EOF

touch $1/__init__.py
mkdir $1/code
touch $1/code/__init__.py

cat <<EOF > $1/code/$1.py
from mpf.system.mode import Mode

class $1(Mode):
    def mode_init(self):
        pass

    def mode_start(self, **kwargs):
        pass

    def mode_stop(self, **kwargs):
        pass
EOF
