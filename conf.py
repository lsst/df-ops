from documenteer.conf.guide import *  # noqa: F401 F403

linkcheck_anchors = False

# Remove this later after we fix documenteer
mermaid_version = "11.9.0"

# Ignore links

linkcheck_ignore = [
    r'https://grafana.slac.stanford.edu.+',
    r'https://.+.slac.stanford.edu.+',
    r'https://confluence.lsstcorp.org.+',
    r'https://github.com/.+',
    r'https://docs.redhat.com.+',
    r'https://slactraining.skillport.com.+',
    r'https://project.lsst.org.+',
    r"https://www.hpc.cam.ac.uk.+",
    r"https://sbnmpc.astro.umd.edu.+",
    r"https://sbnwiki.astro.umd.edu.+"
]

# Reducing number of workers from 5 to 1 seems to result in fewer timeouts.
linkcheck_workers = 1

# Increase number of retries if timeouts still happen.
linkcheck_retries = 3

# disable TLS verification

tls_verify = False
