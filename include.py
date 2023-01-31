import tinytuya as tuya
import conf as c

device = tuya.BulbDevice(
    dev_id    = c.dev_id, 
    address   = c.address,
    local_key = c.local_key,
    version=3.4
)

print(device.status())