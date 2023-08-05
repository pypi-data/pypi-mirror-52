from __future__ import absolute_import

from flytekit.configuration import common as _config_common

URL = _config_common.FlyteRequiredStringConfigurationEntry('platform', 'url')
INSECURE = _config_common.FlyteBoolConfigurationEntry('platform', 'insecure', default=False)
