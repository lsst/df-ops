from documenteer.conf.guide import *  # noqa: F401 F403

# Temporary workaround for Sphinx 8.1.3 compatibility issue with sphinx.ext.ifconfig
# The extension tries to access .rebuild on tuple config values, causing AttributeError
# Since no .. only or .. ifconfig directives are used in the docs, we can safely disable it
if 'sphinx.ext.ifconfig' in extensions:
    extensions.remove('sphinx.ext.ifconfig')

linkcheck_anchors = False

# Remove this later after we fix documenteer
mermaid_version = "11.9.0"
