from __future__ import (unicode_literals, print_function, absolute_import)

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from iotile.cloud.cloud import IOTileCloud
from iotile.ship.exceptions import RecipeActionMissingParameter
from iotile.core.exceptions import ArgumentError
from iotile.core.hw.hwmanager import HardwareManager
from iotile_cloud.api.exceptions import RestHttpBaseException

G_TO_LSB_SCALE_FACTOR = 0.049
HUMIDITY_SCALE_FACTOR = 1024

class CalibratePOD1MStep(object):
    """A Recipe Step used to callibrate the POD-1M

    This step can only be performed through bluetooth
    The steps are:
    1) When Prompted, Scan the Controller QR Code
    2) When Prompted, Scan the QR Code on the top board
    3) When Prompted, User puts POD in jig, then enters the current humidity value
    4) User flips the POD and presses enter.

    Make you run the test on a flat surface. 

    Args:
        uuid (str): uuid of target device
        humidity (int): Optional. Actual humidity value, by default the program 
            prompts the user for the humidity value which is recommended
        cal_humidity (bool): Optional. Default False, flag to determine whether
            humidity should be calibrated
        cal_accel (bool): Optional. Default False, flag to determine whether
            accelerometer should be calibrated
        sample_count (int): Optional. Number of samples to take to determine 
            static offset of accelerometer. Defaults to 128 samples
        post_note (bool): Optional. Defaults False, flag to determine whether to
            post a note onto iotile.cloud on the calibration data.
    """
    REQUIRED_RESOURCES = [('connection', 'hardware_manager')]

    def __init__(self, args):
        if args.get('uuid') is None:
            raise ArgumentError("CalibratePOD1MStep Parameter Missing", parameter_name='uuid')

        self._uuid = args['uuid']
        self._humidity = args.get('humidity')
        self._cal_humidity = args.get('cal_humidity', False)
        self._cal_accel = args.get('cal_accel', False)
        self._sample_count = args.get('sample_count', 128)
        self._post_note = args.get('post_note', False)

        if not HAS_NUMPY:
            raise ArgumentError("You must install numpy to use this ship step", suggestion="pip install numpy")

    def run(self, resources):
        bot_serial_code = input("Scan QR code on BMD module: ")
        top_serial_code = input("Scan QR code on top board: ")

        hw = resources['connection'].hwman
        accel_tile = hw.get(12)
        env_tile = hw.get(14)

        calibration_payload = {}

        calib_manager = accel_tile.calibration_manager()
        setup_manager = accel_tile.setup_manager()
        
        if self._cal_humidity:
            env_tile.set_calibration(0,0,0)
        
            if self._humidity is None:
                actual_humidity = float(input("Set POD in configuration 1 and enter measured humidity: "))
            else:
                actual_humidity = self._humidity
                input("Set POD in configuration 1:")
            
            env_tile.poll_data()
            measured_humidity = env_tile.get_humidity()
            env_offset = int((measured_humidity-actual_humidity)*HUMIDITY_SCALE_FACTOR)

            env_tile.set_calibration(0, env_offset, 0)
            env_tile.persist_calibration()
            env_tile_calib_info = env_tile.calibration_info()

            calibration_payload['env_offset'] = env_offset
            calibration_payload['env_guid'] = str(env_tile_calib_info['serial_number'])
            calibration_payload['env_timestamp'] = str(env_tile_calib_info['calibration_time'])
            
        if self._cal_accel:
            calib_manager.set_calibration(1,1,1,0,0,0)
        
            actual_accel_config1 = np.array([0.5, 0.5,np.sqrt(2)/2])
            setup_manager.start_recording()
            measured_accel_config1 = np.array(calib_manager.static_offset(self._sample_count))*G_TO_LSB_SCALE_FACTOR
            setup_manager.stop_recording()

            if np.sum(measured_accel_config1) < 0:
                setup_manager.stop_recording()
                user_input = input("Sum of vectors is less than 0 when they should all be positive, type [c] to continue: ")
                if user_input != 'c':
                    raise ArgumentError("Not on jig properly", values=measured_accel_config1)
            
            input("Set POD in configuration 2 and then Enter: ")

            actual_accel_config2 = np.array([-0.5, -0.5, -np.sqrt(2)/2])
            setup_manager.start_recording()
            measured_accel_config2 = np.array(calib_manager.static_offset(self._sample_count))*G_TO_LSB_SCALE_FACTOR
            setup_manager.stop_recording()

            if np.sum(measured_accel_config2) > 0:
                setup_manager.stop_recording()
                user_input = input("Sum of vectors is greater than 0 when they should be all negative, type [c] to continue: ")
                if user_input != 'c':
                    raise ArgumentError("Not on jig properly", values=measured_accel_config2)

            #We will calculate gain and offsets, but not actually use those numbers. Will be saved into cloud
            gains = (actual_accel_config1 - actual_accel_config2)/(measured_accel_config1-measured_accel_config2)
            offsets = measured_accel_config1- gains*actual_accel_config1

            #This is the offset that will actually be used. Will average the two opposing perturbations
            offsets_only = (measured_accel_config1+measured_accel_config2)/2

            x_gain   = gains[0]
            x_offset = offsets[0]
            y_gain   = gains[1]
            y_offset = offsets[1]
            z_gain   = gains[2]
            z_offset = offsets[2]

            x_offset_only = offsets_only[0]
            y_offset_only = offsets_only[1]
            z_offset_only = offsets_only[2]

            calib_manager.set_calibration(1, 1, 1, x_offset_only, y_offset_only, z_offset_only)
            calib_manager.persist_calibration()

            acc_tile_calib_info = calib_manager.calibration_info()

            calibration_payload['acc_sample_count'] = self._sample_count
            calibration_payload['acc_x_gain_method_1'] = x_gain
            calibration_payload['acc_y_gain_method_1'] = y_gain
            calibration_payload['acc_z_gain_method_1'] = z_gain
            calibration_payload['acc_x_offset_method_1'] = x_offset
            calibration_payload['acc_y_offset_method_1'] = y_offset
            calibration_payload['acc_z_offset_method_1'] = z_offset
            calibration_payload['acc_x_offset_set'] = x_offset_only
            calibration_payload['acc_y_offset_set'] = y_offset_only
            calibration_payload['acc_z_offset_set'] = z_offset_only
            calibration_payload['acc_guid'] = str(acc_tile_calib_info['serial_number'])
            calibration_payload['acc_timestamp'] = str(acc_tile_calib_info['calibration_time'])
            calibration_payload['bot_serial_code'] = bot_serial_code
            calibration_payload['top_serial_code'] = top_serial_code

        print(calibration_payload)

        if self._post_note:
            self._post_calibration_note(calibration_payload)

            setup_manager.start_recording()
            print("Acc Tile Meas Values: %s" % str(np.array(calib_manager.static_offset(self._sample_count))*G_TO_LSB_SCALE_FACTOR))
            print("Acc Tile Exp  Values: %s" % list(actual_accel_config2))
            print("Env Tile Meas Values: %s %s %s" % (env_tile.sample_humidity(), env_tile.sample_pressure(), env_tile.sample_temperature()))
            print("Env Tile Exp  Values: %s RH" % (actual_humidity))
            setup_manager.stop_recording()

    def _post_calibration_note(self, calibration):
        cloud = IOTileCloud()
        device = cloud.device_info(self._uuid)

        # Post :device:calibration configuration attribute
        payload = {
            'target': device['slug'],
            'name': ':device:calibration',
            'data': calibration,
            'log_as_note': True
        }
        try:
            resp = cloud.api.config.attr.post(payload)
        except RestHttpBaseException as e:
            print('Something failed: {}'.format(e))
