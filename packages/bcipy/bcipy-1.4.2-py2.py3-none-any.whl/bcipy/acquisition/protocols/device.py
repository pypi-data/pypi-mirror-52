"""Interface for creating new device drivers."""
from bcipy.acquisition.device_info import DeviceInfo


class Device():
    """Base class for device-specific behavior.

    Parameters
    ----------
        connection_params : dict
            Parameters needed to connect with the given device
        fs : int
            Sample frequency in Hz.
        channels : list
            List of channel names.
    """

    # pylint: disable=invalid-name
    def __init__(self, connection_params, fs, channels):
        self._connection_params = connection_params
        self.fs = fs
        self.channels = channels

    @property
    def name(self):
        """Device name to be written to the output."""
        raise NotImplementedError('Subclass must define a name property')

    @property
    def device_info(self):
        """Information about the acquisition parameters. Should be called after
        acquisition_init for those devices which set this information."""
        device_name = self.name if not callable(self.name) else self.name()
        return DeviceInfo(fs=self.fs, channels=self.channels, name=device_name)

    def connect(self):
        """Connect to the data source."""
        pass

    def acquisition_init(self):
        """Initialization step. Depending on the protocol, this may involve
        reading header information and setting the appropriate instance
        properties or writing to the server to set params (ex. sampling freq).
        """
        pass

    def read_data(self):
        """Read the next sensor data record from the data source.

        Returns
        -------
            list with a float for each channel.
        """
        raise NotImplementedError(
            'Subclass must define the read_sensor_data method')

    def disconnect(self):
        """Optional method to disconnect from the device and do any cleanup"""
        pass
