from documenteer.conf.guide import *  # noqa: F401 F403

linkcheck_anchors = False

# Remove this later after we fix documenteer
mermaid_version = "11.9.0"

# Ignore links

linkcheck_ignore = [
    r'http://grafana.slac.stanford.edu.+/',
    r'http://docs.redhat.com.+',
]
