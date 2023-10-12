from connectors.OSIPIConnector import OSIPIConnector

from config import (
    OSI_PI_BASE_URL,
    OSI_PI_USERNAME,
    OSI_PI_PASSWORD,
)

# Instatiate the connector for other modules to use
instantiated_osipiconnector = OSIPIConnector(OSI_PI_BASE_URL, OSI_PI_USERNAME, OSI_PI_PASSWORD)