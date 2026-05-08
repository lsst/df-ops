from documenteer.conf.guide import *  # noqa: F401 F403

linkcheck_anchors = False

# Remove this later after we fix documenteer
mermaid_version = "11.9.0"

# Ignore links

linkcheck_ignore = [
    r'https://grafana.slac.stanford.edu.+',
    r'https://k8s.slac.stanford.edu.+',
    r'https://github.com/slaclab.+',
    r'https://docs.redhat.com.+',
    r'https://slactraining.skillport.com.+',
]

# disable TLS verification

tls_verify = False
