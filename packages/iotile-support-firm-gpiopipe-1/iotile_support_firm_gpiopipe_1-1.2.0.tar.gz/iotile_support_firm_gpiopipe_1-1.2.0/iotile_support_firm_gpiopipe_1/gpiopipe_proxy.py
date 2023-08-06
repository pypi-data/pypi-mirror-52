"""Proxy module for the firm_gpiopipe firmware."""

import struct
from time import sleep
import sys
from binascii import hexlify
from time import monotonic

from iotile.core.hw.proxy.proxy import TileBusProxyObject
from iotile.core.hw.proxy.plugin import TileBusProxyPlugin
from iotile.core.utilities.typedargs.annotate import annotated, param, return_type, context, docannotate
from iotile.core.exceptions import ArgumentError, HardwareError

from .pipeline_result import PipelineResult

def _format_string(signed):
    """module level internal function for conciseness"""
    return "l" if signed else "L"


@context("GPIOPipelineProxy")
class GPIOPipelineProxy(TileBusProxyObject):
    """Proxy module for pipelined gpio firmware.


    :param stream: CMDStream instance that can communicate with this tile
    :param addr: Local tilebus address of this tile
    """

    NUM_PIPELINES = 4

    def __init__(self, stream, addr):
        super(GPIOPipelineProxy, self).__init__(stream, addr)

        self._resource_manager = ResourceManager(self)
        self._pipeline_manager = PipelineManager(self)

    @classmethod
    def ModuleName(cls):
        return 'gppip1'

    @annotated
    def resource_manager(self):
        """Plugin object for querying the current status of on-chip resources."""
        return self._resource_manager

    @annotated
    def pipeline_manager(self):
        """Plugin object for managing pipelines in real time."""

        return self._pipeline_manager

    @param("pipeline", "integer", "nonnegative", desc='The pipeline to query')
    @param("value", "integer", desc='The trigger value to feed into the pipeline')
    @param("signed", "bool", desc='Default False. True if trigger value is signed.')
    def trigger_pipeline(self, pipeline, value, signed=False):
        """Feed pipeline a value.

        Defaults to an unsigned value. Pass signed=True if signed value.

        """
        if pipeline >= GPIOPipelineProxy.NUM_PIPELINES:
            raise ArgumentError("Invalid pipeline number", pipeline=pipeline)

        err, = self.rpc(0x80, 0x30 + pipeline, value, arg_format=_format_string(signed), result_format="L")

        if err != 0:
            raise HardwareError("Error triggering pipeline", error_code=err, pipeline=pipeline)

    @return_type("integer")
    @param("pipeline", "integer", "nonnegative", desc='The pipeline to query')
    @param("signed", "bool", desc='Default False. True if output value is signed.')
    def last_value(self, pipeline, signed=False):
        """Get the current value of a processing pipeline.

        You should pass an integer from 0 to kNumPipelines to get the last value of a
        pipeline.
        """

        if pipeline >= GPIOPipelineProxy.NUM_PIPELINES:
            raise ArgumentError("Invalid pipeline number", pipeline=pipeline)

        value, = self.rpc(0x80, pipeline, result_format=_format_string(signed))
        return value

    @docannotate
    def last_result(self, result, default=None):
        """Get the last value pushed into a given result.

        This RPC inspects the value currently stored in the given result
        object and returns its value.  If there has never been a value pushed
        to the result, then by default a HardwareError is raised.

        However, you can specify a default value to return instead by using
        the optional default parameter.  If the result object you are
        referencing have not be setup up then an exception will be raised.

        You can configure results by using the `pipeline_manager`.

        Args:
            result (int): The index of the result that you wish to inspect.
            default (int): Optional default value to return if the result
                has never had a value pushed to it.  If not specified, an
                exception will be raised for empty results.

        Returns:
            int format-as hex: The current value of the result.
        """

        info = self._pipeline_manager.result_inspect(result)

        value = info.get_value(default)
        if value is None:
            raise HardwareError("Result %d is empty and no default value given" % result)

        return value

    @return_type("integer")
    @param("pipeline", "integer", "nonnegative", desc='The pipeline to query')
    @param("stage", "integer", "nonnegative", desc='The stage to inspect')
    @param("signed", "bool", desc='Default False. True if output value is signed.')
    def inspect_stage(self, pipeline, stage, signed=False):
        """Get the current value of a processing pipeline stage.

        You should pass an integer from 0 to kNumPipelines and a stage number
        from 0 to the total number of stages.
        """

        if pipeline >= GPIOPipelineProxy.NUM_PIPELINES:
            raise ArgumentError("Invalid pipeline number", pipeline=pipeline)

        value, = self.rpc(0x80, 0x10, pipeline, stage, arg_format="BB", result_format=_format_string(signed))
        return value

    @param("pipeline", "integer", "nonnegative", desc='The pipeline to query')
    @param("stage", "integer", "nonnegative", desc='The stage to inspect')
    @param("signed", "bool", desc='Default False. True if output value is signed.')
    def watch_stage(self, pipeline, stage, signed=False):
        """Poll and print the values of the pipeline stage.

        The values are printed over each other until you hit the enter
        key then a timestamp is printed with the value and a new line
        is started.

        Stop the process by hitting Control-C

        You should pass an integer from 0 to kNumPipelines and a stage number
        from 0 to the total number of stages.
        """

        try:
            print("Starting watch of pipeline %d, stage %d" % (pipeline, stage))
            while True:
                sys.stdout.write('\r' + (' '*40) + '\r')
                value = self.inspect_stage(pipeline, stage, signed)
                sys.stdout.write(str(value))
                sys.stdout.flush()
                sleep(0.1)
        except KeyboardInterrupt:
            pass

        print("\nFinished")

    @return_type("integer")
    @param("pipeline", "integer", "nonnegative", desc='The pipeline to query')
    def run_count(self, pipeline):
        """Get the count of how many times this pipeline has been run.

        You should pass an integer from 0 to kNumPipelines.
        """

        if pipeline >= GPIOPipelineProxy.NUM_PIPELINES:
            raise ArgumentError("Invalid pipeline number", pipeline=pipeline)

        value, = self.rpc(0x80, 0x11, pipeline, arg_format="B", result_format="L")
        return value


@context("ResourceManager")
class ResourceManager(TileBusProxyPlugin):
    """A proxy plugin for getting the status of used chip resources."""

    # This must stay in sync with resource.h inside the firmware
    RESOURCE_NAMES = {
        0: "Main Clock",
        1: "High Power Periodic Task",
        2: "Low Power Periodic Task",
        3: "Pin Interrupt Task",
        4: "Low Power RTC Task"
    }

    @return_type("map(string, integer)")
    def current_usage(self):
        """Get the current request count of all known resources."""

        res = self.rpc(0x80, 0x60, result_format="20B")
        length = res[0]
        if length == 0:
            return {}

        res = res[1:1+length]

        return {self.RESOURCE_NAMES[i]: res[i] for i in range(0, len(res))}

    @return_type("map(string, integer)")
    def resource_limits(self):
        """Get the allocated and available heap and pipeline resources."""

        total_heap, prealloc, total_alloc, max_pipe, max_stage = self.rpc(0x80, 0x61, result_format="HHHHH6x")

        return {
            'total_heap': total_heap,
            'preallocated_size': prealloc,
            'total_allocated_heap': total_alloc,
            'max_pipelines': max_pipe,
            'max_stages': max_stage
        }


@context("PipelineManager")
class PipelineManager(TileBusProxyPlugin):
    """A proxy plugin for modifying a pipeline running on the tile in realtime."""

    _dry_run = False
    _stages = []
    _results = []
    _current_config = None
    _current_handler = None

    HANDLERS = {
        'identity': 0,
        'periodic_trigger': 1,
        'adc': 2,
        'windowed_threshold': 3,
        'decimator': 4,
        'accumulator': 5,
        'edge_detect': 6,
        'lut':7,
        'digital': 8,
        'pulse_characterize': 9,
        'pulse_qualify': 10,
        'digital_combine': 11,
        'iir': 12
    }

    @param("dry_run", "bool", desc="Don't actually execute the pipeline commands, just capture them")
    def begin_capture(self, dry_run=True):
        """Capture the pipelines that are being created.

        This saves off the config information required to recreate these
        same pipelines later.  This is useful for saving config variables
        that contain those pipeline configurations.
        """

        self._dry_run = dry_run
        self._stages = []
        self._results = []
        self._current_config = None
        self._current_handler = None

    @return_type("list(string)")
    def finish_capture(self):
        """Return the captured configuration.

        This method will convert any pipeline or result configuration steps
        that have happened since the last call to begin_capture into the
        corresponding binary values that should be placed into config
        variables in order to achieve the same configuration in a persistent
        fashion.
        """

        heap_data = bytearray()
        stage_data = bytearray()
        result_data = bytearray()

        for pipeline, stage, handler, config in self._stages:
            if config is not None:
                if len(config) % 4 != 0:
                    config += bytearray(b'\0' * (4 - (len(config) % 4)))

                assert len(config) % 4 == 0
                config_length = len(config)
            else:
                config_length = 0

            stage_entry = struct.pack("<BBBB", pipeline, stage, handler, config_length)

            if config_length > 0:
                heap_data += config

            stage_data += stage_entry

        for result in self._results:
            result_data += bytearray(result.encode())

        lines = []

        if len(stage_data) > 0 or len(heap_data) > 0:
            lines.append("0x8000: hex:%s" % _hex_str(heap_data))
            lines.append("0x8001: hex:%s" % _hex_str(stage_data))

        if len(result_data) > 0:
            lines.append("0x8006: hex:%s" %  _hex_str(result_data))

        return lines

    @docannotate
    def result_reset(self, index):
        """Clear a previously enabled result resource.

        This will disable the result and clear any stored settings.  If the
        result was configured via a config variable at boot time, that config
        variable will still be active so the result will be re-enabled at the
        next tile reset.

        If the result is not configured, nothing will be done and no error
        will be thrown so this method is safe to call for any result resource.

        Args:
            index (int): The index of the result that you wish to clear.
        """

        err, = self.rpc_v2(0x8092, "B", "L", index)
        if err != 0:
            raise HardwareError("Error 0x%08X clearing result %d" % (err, index))

    @docannotate
    def result_inspect(self, index):
        """Inspect the configuration of a result resource.

        This will query the result from the tile and return its configuration
        and state as a PipelineResult object.

        Args:
            index (int): The index of the result that you wish to query.

        Returns:
            PipelineResult show-as string: The result's configuration and state.
        """

        binary_config, flags, value = self.rpc_v2(0x8090, "H", "15sBL", index)


        result = PipelineResult.FromBinary(index, binary_config, flags, value)
        if result is None:
            raise ArgumentError("Result %d is not defined" % index)

        return result

    @docannotate
    def result_state(self, index):
        """Query whether the result is updated, changed or old.

        This will query whether the result from the tile has been updated
        since the last call to result_touch().  The possible return values
        are:
        - nothing
        - updated
        - changed
        - same

        Args:
            index (int): The index of the result that you wish to query.

        Returns:
            str: A string indicating the result's status.
        """

        result = self.result_inspect(index)
        return result.state


    @docannotate
    def result_config(self, index, config_string, force=False):
        """Set the configuration of a result.

        A "result" object produces a single 32-bit value from 1-4 source
        pipeline stages.  The stages can come from any pipeline and do not
        have to be unique, i.e. the same stage could be used multiple times if
        you want.

        The result's value can be specified to pull specific bits from each
        source and combine them together into a single 32-bit value.

        This value can optionally be pushed to another tile (usually the
        controller) every time it is updated or when its numerical value
        changes.

        The configuration of the result is specified in a domain-specific
        minilanguage.

        The general format of the configuration is:
        BITMASK [push to TILE:STREAM [on (change | update)]][,SOURCE_STAGE]*

        The formal format of SOURCE_STAGE is:
        pipeline PIPE[.STAGE][START-END]

        where PIPE, STAGE, START and END are all decimal integers.  If STAGE
        is not specified then it defaults to the final stage in the pipeline.

        START is the first bit selected from the pipeline stage and END is one
        past the last bit selected, so [0-32] specifies the entire 32-bit
        stage value and [0-1] selects a single bit.

        Basically, you specify a BITMASK that declares where each bit in the
        result should come from.  Then you map each part of that bitmask to a
        specific set of bits inside of a pipeline stage.  By default, the
        result is not pushed to any other tile.  You can download its current
        result by calling `last_result` from the proxy.  You can also set up
        the result to automatically push a value to another tile by adding a
        'push to' section of the config.  `push to 8:0xff on change` would
        cause the result to be pushed to the controller's sensor_graph input
        in input stream 255 every time the value of the result numerically
        changed.  `push to 8:0xff on update` will have the same behavior but
        trigger a push every time the value is updated, even if it has the
        same numerical value as the previous result.

        Depending on the source of the values used in the result, it may make
        more sense to use either `on update` or `on change`.  The result is
        considered to be updated whenever any pipeline stage that feeds it
        updates its value.

        The best way to document the format for BITMASK and SOURCE_STAGE is
        via examples.

        For example, to just load all of pipline 1 stage 4 into the result, you
        would do:

        32a, a: pipeline 1.4[0-32]

        If you wanted to pull the 20 low bits from pipeline 0 stage 1 and the
        12 high bits from pipeline 1 stage 2, it would be:

        20a12b, a: pipeline 0.1[0-20], b: pipeline 1.2[20-32]

        You can also specify reserved bits that are set to zero such as:

        20a12x, a: pipeline 0.1[0-20]

        This will take the low 20 bits from pipeline 0 stage 1 and leave the 12
        high bits clear.  Reserved space can be located anywhere in the bitmask,
        such as:

        4a24x4b, a: pipeline 0.1[0-4], b: pipeline 1.2[0-4]

        The value between the brackets after each pipeline are the start and
        end bits that should be taken from that pipeline stage.  There is no
        requirement that the bit index into the pipeline stage matches where
        it is placed into the result.

        The letters used to identify each pipeline stage are arbitrary and can
        be any lowercase value (except x which is reserved to denote zero
        bits).

        There can be a maximum of 4 pipeline sources for each result and the
        reserved bits count as a pipeline source.  So the bitmask of 4a20x4b4c
        is okay because it has 4 sources but 4a16x4b4c4d would not be allowed
        because it has 5 sources.

        If you want to load a result with the final stage from a pipeline then
        the [.STAGE] portion of the SOURCE_STAGE may be omitted.  The [a-b] bit
        specifiers currently must always be present and are checked to make sure
        they agree in size with the space being allocated in the BITMASK.

        The bitmask must always contain exactly 32 bits.

        Args:
            index (int): The index of the result that we would like to configure
            config_string (str): The configuration descriptor.  See the docstring
                for this method to understand the format for the configuration
                descriptor.
            force (bool): Optional parameter specifying whether to silently
                overwrite any existing configuration or throw an error if the
                result is not empty.
        """

        result = PipelineResult.FromString(index, config_string)

        self._results.append(result)
        if self._dry_run:
            return

        error, = self.rpc_v2(0x8091, "BB15s", "L", index, int(force), result.encode())
        if error != 0:
            raise HardwareError("Unable to configure result %d: 0x%08x" % (index, error),
                                config=config_string, force=force)

    @param("pipeline", "integer", "nonnegative", desc='The pipeline to reset')
    def pipeline_reset(self, pipeline):
        """Clear all stages and reset a processing pipeline.

        This function is useful when you want to test out various pipeline
        configurations.
        """

        if pipeline >= GPIOPipelineProxy.NUM_PIPELINES:
            raise ArgumentError("Invalid pipeline number", pipeline=pipeline)

        err, = self.rpc(0x80, 0x20, pipeline, arg_format="B", result_format="L")
        if err != 0:
            raise HardwareError("Error clearing pipeline", error_code=err, pipeline=pipeline)

    @param("pipeline", "integer", "nonnegative", desc='The pipeline to modify')
    @param("stage", "integer", "nonnegative", desc='The stage to modify')
    @param("pin", "integer", "nonnegative", desc="The pin to use for analog measurement")
    @param("power_pin", "integer", desc="The pin to use for power (optional)")
    @param("delay", "integer", "nonnegative", desc="The number of milliseconds to delay between power and measurement")
    @param("invert_power", "bool", desc="True if the power pin is active low, defaults to False")
    @param("power_always", "bool", desc="True if the power pin if always on, defaults to False")
    @param("keep_enabled", "bool", desc="True if the adc should remain enabled at all times")
    def add_stage_adc_convert(self, pipeline, stage, pin, power_pin=None, delay=0, invert_power=False, power_always=False, keep_enabled=True):
        """Add a pipeline stage that takes an analog measurement.

        The measurement is performed every time the pipeline stage is triggered.
        You can optionally specify another pin that should be pulsed during the
        measurement in order to provide power to the analog source.  You can
        delay between 0 and 65536 ms between power application and measurement.

        If the power pin is active low you should pass the invert_power flag.
        The power pin defaults to off whenever a measurement is not in progress.
        power_always can also be set True so that power will always be on.
        """

        self._begin_pipeline_stage(self.HANDLERS['adc'], 6)

        apply_power = int(power_pin is not None)
        invert_power = int(invert_power)
        keep_enabled = int(keep_enabled)
        if not apply_power:
            power_pin = 0
        config = struct.pack("<BBBBH", pin, power_pin, ((apply_power << 0) | (invert_power << 1) | (keep_enabled << 2) | (power_always << 3)), 0, delay)
        self._load_pipeline_stage_config(config)
        self._finish_pipeline_stage(pipeline, stage)

    @param("pipeline", "integer", "nonnegative", desc='The pipeline to modify')
    @param("stage", "integer", "nonnegative", desc='The stage to modify')
    @param("pin", "integer", "nonnegative", desc="The pin to use for digital measurement")
    @param("power_pin", "integer", desc="The pin to use for power (optional)")
    @param("delay", "integer", "nonnegative", desc="The number of milliseconds to delay between power and measurement")
    @param("invert_power", "bool", desc="True if the power pin is active low, defaults to False")
    @param("power_always", "bool", desc="True if the power pin if always on, defaults to False")
    @param("pull_config", "string", ("list", ["pullup","pulldown","inactive"]), desc='internal pullup/down configuration')
    def add_stage_digital_sample(self, pipeline, stage, pin, power_pin=None, delay=0, invert_power=False, power_always=False, pull_config='pullup'):
        """Add a pipeline stage that takes an digital measurement.

        The measurement is performed every time the pipeline stage is
        triggered. You can optionally specify another pin that should be
        pulsed during the measurement in order to provide power to the digital
        source.  You can delay between 0 and 65536 ms between power
        application and measurement.

        If the power pin is active low you should pass the invert_power flag.
        The power pin defaults to off whenever a measurement is not in
        progress. power_always can also be set True so that power will always
        be on.
        """
        pullup_configs = {
            'pullup': 2,
            'pulldown': 1,
            'inactive': 0
        }

        self._begin_pipeline_stage(self.HANDLERS['digital'], 6)

        apply_power = int(power_pin is not None)
        invert_power = int(invert_power)
        if not apply_power:
            power_pin = 0
        config = struct.pack("<BBBBH", pin, power_pin, ((apply_power << 0) | (invert_power << 1) | (power_always << 2) | (pullup_configs[pull_config] << 3)), 0, delay)
        self._load_pipeline_stage_config(config)
        self._finish_pipeline_stage(pipeline, stage)

    @param("pipeline", "integer", "nonnegative", desc='The pipeline to modify')
    @param("stage", "integer", "nonnegative", desc='The stage to modify')
    @param("pin", "integer", "nonnegative", desc="The pin to use for digital measurement")
    @param("power_pin", "integer", desc="The pin to use for power (optional)")
    @param("delay", "integer", "nonnegative", desc="The number of milliseconds to delay between power and measurement")
    @param("invert_power", "bool", desc="True if the power pin is active low, defaults to False")
    @param("power_always", "bool", desc="True if the power pin if always on, defaults to False")
    @param("pull_config", "string", ("list", ["pullup","pulldown","inactive"]), desc='internal pullup/down configuration')
    @param("operation", "string", ("list", ["and","or","nand","nor","xor","xnor","encode"]), desc='operation to peform on previous and current reading')
    def add_stage_digital_sample_combine(self, pipeline, stage, pin, power_pin=None, delay=0, invert_power=False, power_always=False, pull_config='pullup', operation='and'):
        """Add a pipeline stage that takes an digital measurement and performs
        and operation with the current and previous digital_sample stage.

        This stage is meant to come after the digital sample stage. It takes
        the previous stage result and performs a specified operation on both results
        to create the new result

        The measurement is performed every time the pipeline stage is
        triggered. You can optionally specify another pin that should be
        pulsed during the measurement in order to provide power to the digital
        source.  You can delay between 0 and 65536 ms between power
        application and measurement.

        If the power pin is active low you should pass the invert_power flag.
        The power pin defaults to off whenever a measurement is not in
        progress. power_always can also be set True so that power will always
        be on.
        """
        pullup_configs = {
            'pullup': 2,
            'pulldown': 1,
            'inactive': 0
        }

        combine_op_configs = {
            'and': 0,
            'or': 1,
            'nand': 2,
            'nor': 3,
            'xor': 4,
            'xnor': 5,
            'encode': 6
        }

        self._begin_pipeline_stage(self.HANDLERS['digital_combine'], 6)

        apply_power = int(power_pin is not None)
        invert_power = int(invert_power)
        if not apply_power:
            power_pin = 0
        config = struct.pack("<BBBBH", pin, power_pin, ((apply_power << 0) | (invert_power << 1) | (power_always << 2) | (pullup_configs[pull_config] << 3) | (combine_op_configs[operation] << 5)), 0, delay)
        self._load_pipeline_stage_config(config)
        self._finish_pipeline_stage(pipeline, stage)

    @param("pipeline", "integer", "nonnegative", desc='The pipeline to modify')
    @param("stage", "integer", "nonnegative", desc='The stage to modify')
    @param("pin", "integer", "nonnegative", desc="The pin to use for analog measurement")
    @param("rising", "bool", desc="Detect on the rising (True) or falling (False")
    @param("throttle", "float", desc="Minimum time between multiple events (in ms)")
    def add_stage_edge_detect(self, pipeline, stage, pin, rising, throttle=0):
        """Add a pipeline stage that triggers on a pin edge.

        You can configure the pin to any GPIO pin and trigger on either the
        rising or falling edges.
        """

        # The internal lpfilter logic works in 100 us ticks, so convert ms to ticks
        throttle = int(throttle * 10)

        self._begin_pipeline_stage(self.HANDLERS['edge_detect'], 4)

        edge = 1 << int(rising)
        config = struct.pack("<BBH", pin, edge, throttle)
        self._load_pipeline_stage_config(config)
        self._finish_pipeline_stage(pipeline, stage)

    @param("pipeline", "integer", "nonnegative", desc='The pipeline to modify')
    @param("stage", "integer", "nonnegative", desc='The stage to modify')
    @param("base_freq", "integer", "nonnegative", desc='The base frequency for the underlying timer resource')
    @param("interval", "integer", "nonnegative", desc='The number of timer ticks per pipeline wakeup')
    @param("low_power", "bool", desc="True to use a low power (imprecise timer)")
    def add_stage_periodic_trigger(self, pipeline, stage, base_freq, interval, low_power=False):
        """Add a pipeline stage that triggers the pipeline periodically.

        You can trigger a pipeline every X ticks by adding this pipeline stage.
        The tick can either be generated by the main clock, in which case the chip
        can never sleep or by a low power clock which works regardless of chip sleep
        status but is +-40% tolerance so its very inaccurate.
        """

        self._begin_pipeline_stage(self.HANDLERS['periodic_trigger'], 12)

        config = struct.pack("<LLBBH", base_freq, interval, int(low_power), 0, 0)
        self._load_pipeline_stage_config(config)
        self._finish_pipeline_stage(pipeline, stage)

    @param("pipeline", "integer", "nonnegative", desc='The pipeline to modify')
    @param("stage", "integer", "nonnegative", desc='The stage to modify')
    @param("min_entering", "integer", "nonnegative", desc='The lower window threshold when entering the window')
    @param("min_leaving", "integer", "nonnegative", desc='The lower window threshold when leaving the window')
    @param("max_entering", "integer", "nonnegative", desc='The upper window threshold when entering the window')
    @param("max_leaving", "integer", "nonnegative", desc='The upper window threshold when leaving the window')
    @param("only_inside", "bool", desc='Ignore all values outside the window rather than passing them as 0')
    @param("pass_raw", "bool", desc='Pass the raw input value instead of 0 or 1, most useful when combined with only_inside')
    def add_stage_windowed_threshold(self, pipeline, stage, min_entering, min_leaving, max_entering, max_leaving, only_inside=False, pass_raw=False):
        """Add a pipeline stage that does a window comparison with optional hysteresis.

        This pipeline stage outputs a 1 if the input value is inside a [min, max] range
        and 0 otherwise.  It remembers if the last input was inside or outside of the range
        and can have two different bounds to allow for hysteretic thresholding like a schmidt
        thrigger.

        If you do not want any hysteresis, just enter the same window values for both
        entering and leaving.
        """

        self._begin_pipeline_stage(self.HANDLERS['windowed_threshold'], 20)

        config = struct.pack("<LLLLL", min_entering, min_leaving, max_entering, max_leaving, (int(only_inside) << 0) | (int(pass_raw) << 1))
        self._load_pipeline_stage_config(config)
        self._finish_pipeline_stage(pipeline, stage)

    @param("pipeline", "integer", "nonnegative", desc='The pipeline to modify')
    @param("stage", "integer", "nonnegative", desc='The stage to modify')
    @param("decimation_rate", "integer", "nonnegative", desc='The decimation ratio N (N:1 samples in to out)')
    @param("operation", "string", ("list", ["min", "max", "identity", "glitch", "one"]), desc='operation')
    @param("only_change", "bool", desc='only pass on values that are different from that past output')
    def add_stage_decimator(self, pipeline, stage, decimation_rate, operation, only_change=False):
        """Add a pipeline stage that performs a decimation filter on the input

        This stage will output 1 sample for every decimation_rate input samples.
        You can choose how the output sample will be calculated by specifying the
        operation.  For example, you can output the maximum input seen, the
        minimum input seen, or just output every Nth sample.

        You can optionally pass only_change=True to make this an edge detection filter.
        Edge detection works by comparing a value about to be output to the last output
        value.  If they are the same, the value is discarded and nothing is output but
        the decimator is reset.
        """

        decimation_ops = {
            'identity': 0,
            'min': 1,
            'max': 2,
            'glitch': 3,
            'one': 4
        }

        flags = int(only_change) << 0

        self._begin_pipeline_stage(self.HANDLERS['decimator'], 4)

        config = struct.pack("<HBB", decimation_rate, decimation_ops[operation], flags)
        self._load_pipeline_stage_config(config)
        self._finish_pipeline_stage(pipeline, stage)

    # IIR Filter stage addition
    @param("pipeline", "integer", "nonnegative", desc='The pipeline to modify')
    @param("stage", "integer", "nonnegative", desc='The stage to modify')
    @param("coeff", "integer", ("range", 0, 0xFFFF), desc='IIR filter coefficient 0-0xFFFF')
    def add_stage_iir(self, pipeline, stage, coeff):
        """ Add a pipeline stage that performs a first order iir filter on the input
                X_curr = ADC_VALUE_12bits << 4
                X_prev = (C * X_prev) + ((1-C) * X_curr)

                Input of the IIR stage is expected to be a 12bit adc value.
                The coefficient is a 16bit fixed point representation where:
                    1 = 0x10000, 0.5 = 0x07FFF, 0 = 0x00000
                    Larger coefficient == more filtering
                    0 = filter disabled.
        """

        self._begin_pipeline_stage(self.HANDLERS['iir'], 4)
        config = struct.pack("<HH", coeff, 0)
        self._load_pipeline_stage_config(config)
        self._finish_pipeline_stage(pipeline, stage)

    # LUT: Stage Addition
    @param("pipeline", "integer", "nonnegative", desc='The pipeline to modify')
    @param("stage", "integer", "nonnegative", desc='The stage to modify')
    @param("input_is_signed", "bool", desc='Input to lut is signed')
    @param("output_is_signed", "bool", desc='Output of lut is signed')
    @param("extrapolate", "bool", desc='Extrapolate outside of table bounds')
    @param("interpolate", "bool", desc='Interpolate between table entries')
    @param("itbl", "list(integer)", desc='Input Table')
    @param("otbl", "list(integer)", desc='Output Table')
    def add_stage_lut(self, pipeline, stage, itbl, otbl,
            input_is_signed=False, output_is_signed=False, extrapolate=True, interpolate=True ):
        """Add a pipeline stage that performs a LUT map on the input
        """

        # Test lut
        #itbl = [100, 200, 300, 400, 500, 600, 700, 800];
        #otbl = [10, 200, 1000, 4000, 1000, 8000, 1000, 16000];
        #input_is_signed = 0;
        #output_is_signed = 0;
        #extrapolate = 0;
        #interpolate = 1;

        is_valid = 1;

        if input_is_signed:
            if len([x for x in itbl if x < -0x80000000 or x > 0x7FFFFFFF]) > 0:
                raise ArgumentError("Not all input LUT Values are int32_t values", pipeline=itbl)
            input_table_packet = struct.pack("<8l", *itbl)
        else:
            if len([x for x in itbl if x < 0x00000000 or x > 0xFFFFFFFF]) > 0:
                raise ArgumentError("Not all input LUT Values are uint32_t values", pipeline=itbl)
            input_table_packet = struct.pack("<8L", *itbl)

        if output_is_signed:
            if len([x for x in otbl if x < -0x80000000 or x > 0x7FFFFFFF]) > 0:
                raise ArgumentError("Not all output LUT Values are int32_t values", pipeline=otbl)
            output_table_packet = struct.pack("<8l", *otbl)
        else:
            if len([x for x in otbl if x < 0x00000000 or x > 0xFFFFFFFF]) > 0:
                raise ArgumentError("Not all output LUT Values are uint32_t values", pipeline=otbl)
            output_table_packet = struct.pack("<8L", *otbl)

        self._begin_pipeline_stage(self.HANDLERS['lut'], 72)
        config = input_table_packet + output_table_packet + struct.pack("<BBBBBBBB", 0, 0, 0, \
            input_is_signed, output_is_signed, extrapolate, interpolate, is_valid)
        self._load_pipeline_stage_config(config)
        self._finish_pipeline_stage(pipeline, stage)

    @param("pipeline", "integer", "nonnegative", desc='The pipeline to modify')
    @param("stage", "integer", "nonnegative", desc='The stage to modify')
    @param("glitch", "integer", "nonnegative", desc="The number of repeat measurements needed before certifying a change")
    def add_stage_changedetect(self, pipeline, stage, glitch=1):
        """Add a pipeline stage that only outputs value changes.

        This stage is built on top of a decimation stage with the only_changes
        flag set.  If glitch is passed, then the decimation stage will be placed
        into glitch mode and require X identical samples before updating.
        """

        self.add_stage_decimator(pipeline, stage, glitch, 'glitch', only_change=True)

    @param("pipeline", "integer", "nonnegative", desc='The pipeline to modify')
    @param("stage", "integer", "nonnegative", desc='The stage to modify')
    @param("active_high", "bool", desc="True if on means high (default), 0 if low means on")
    def add_stage_pulse_characterize(self, pipeline, stage, active_high=1):
        """Add a pipeline stage that outputs pulse data

        This stage outputs two uint16 values into a single uint32 value. first value is
        number of samples the pulse is off for, second value is number of samples the pulse is
        on for. active_high by default is true, which means it determines the pulse as 'on'
        when the reading is high, set to false if 'on' means a low reading
        """
        self._begin_pipeline_stage(self.HANDLERS['pulse_characterize'], 4)

        config = struct.pack("<L", active_high)
        self._load_pipeline_stage_config(config)
        self._finish_pipeline_stage(pipeline, stage)

    @param("pipeline", "integer", "nonnegative", desc='The pipeline to modify')
    @param("stage", "integer", "nonnegative", desc='The stage to modify')
    def add_stage_accumulator(self, pipeline, stage):
        """Add an accumulator that adds its inputs.

        The accumulator always outputs the current value of its internal 32-bit
        accumulator every time an input is received (after adding the input).

        This can be used effectively as an event counter, especially when combined
        with thresholding or other stages that output only 0 or 1.
        """

        self._begin_pipeline_stage(self.HANDLERS['accumulator'], 0)
        self._finish_pipeline_stage(pipeline, stage)

    @param("pipeline", "integer", "nonnegative", desc='The pipeline to modify')
    @param("stage", "integer", "nonnegative", desc='The stage to modify')
    @param("on_cond", "string", ("list", ["gt","ge","lt","le","in","ex","true","false"]), \
        desc='Operator used to compare on samples measured and threshold value')
    @param("on_threshold", "integer", "nonnegative", desc='Threshold number of on samples')
    @param("off_cond", "string", ("list", ["gt","ge","lt","le","in","ex","true","false"]), \
        desc='Operator used to compare off samples measured and threshold value')
    @param("off_threshold", "integer", "nonnegative", desc='Threshold number of off samples')
    @param("operation", "string", ("list", ["and","or"]), desc='Operation applied on both on and off conditionals to give final output')
    @param("on_threshold_lower", "integer", "nonnegative", desc='Lower threshold number of on samples if in between operation is used (optional)')
    @param("off_threshold_lower", "integer", "nonnegative", desc='Lower threshold number of off samples if in between operation is used (optional)')
    def add_stage_pulse_qualify(self, pipeline, stage, on_cond, on_threshold, off_cond, off_threshold, operation, \
        on_threshold_lower=0, off_threshold_lower=0):
        """Add a pipeline stage that processes the output of pulse characteize stage

        This stage will output 1 sample for every decimation_rate input samples.
        You can choose how the output sample will be calculated by specifying the
        operation.  For example, you can output the maximum input seen, the
        minimum input seen, or just output every Nth sample.

        You can optionally pass only_change=True to make this an edge detection filter.
        Edge detection works by comparing a value about to be output to the last output
        value.  If they are the same, the value is discarded and nothing is output but
        the decimator is reset.
        """

        conditional_ops = {
            "ge":   0, #Greater or equal
            "gt":   1, #Greater
            "le":   2, #Less or equal
            "lt":   3, #Less
            "in":   4, #Inclusive
            "ex":   5, #Exclusive
            "true": 6, #True
            "false":7  #False
        }

        comparator_ops = {
            "and": 0,
            "or": 1
        }

        self._begin_pipeline_stage(self.HANDLERS['pulse_qualify'], 12)

        config = struct.pack("<HHHHL", on_threshold, on_threshold_lower, off_threshold, off_threshold_lower, \
            (conditional_ops[on_cond] | (conditional_ops[off_cond] << 4) | (comparator_ops[operation] << 8)))
        self._load_pipeline_stage_config(config)
        self._finish_pipeline_stage(pipeline, stage)

    @param("pipeline", "integer", "nonnegative", desc='The pipeline to time')
    @param("interval", "float", "nonnegative", desc='The number of seconds to time for')
    @return_type("float")
    def profile_pipeline(self, pipeline, interval):
        """Calculate the number of times the pipeline executes per second.

        Since a pipeline only executes when a trigger is received, this is
        equivalent to counting the average number of triggers per second,
        over the measurement interval.
        """

        start = self._proxy.run_count(pipeline)
        now = monotonic()
        sleep(interval)
        end = self._proxy.run_count(pipeline)
        delta = monotonic() - now

        return (end - start) / delta

    def _begin_pipeline_stage(self, handler, config_size):
        """Begin a new pipeline stage."""

        self._current_handler = handler
        self._current_config = None

        if self._dry_run:
            return

        err, = self.rpc(0x80, 0x50, config_size, handler, arg_format="HB", result_format="L")
        if err != 0:
            raise HardwareError("Error beginning new pipeline stage", error_code=err)

    def _load_pipeline_stage_config(self, config_data):
        """Load config data into a pipeline stage."""

        self._current_config = config_data
        if self._dry_run:
            return

        for i in range(0, len(config_data), 18):
            chunk = config_data[i:i+18]

            err, = self.rpc(0x80, 0x51, i, chunk, arg_format="H%ds" % len(chunk), result_format="L")
            if err != 0:
                raise HardwareError("Error pushing pipeline stage config data", error_code=err, offset=i, chunk_length=len(chunk))

    def _finish_pipeline_stage(self, pipeline, stage):
        """Finish loading a pipeline stage."""

        self._stages.append((pipeline, stage, self._current_handler, self._current_config))

        if self._dry_run:
            return

        err, = self.rpc(0x80, 0x52, pipeline, stage, arg_format="BB", result_format="L")
        if err != 0:
            raise HardwareError("Error finishing pipeline stage", error_code=err, pipeline=pipeline, stage=stage)

    @return_type("integer")
    def initialization_error(self):
        """Check if there was any error initializing a pipeline on reset.

        Errors can be thrown on intialization if there are pipeline stages configured
        via config variables and those variables are incorrectly configured.
        """

        init_error, = self.rpc(0x80, 0x61, result_format="12xL")

        return init_error


def _hex_str(input_data):
    """Ensure that we have a str of hex, not bytes on python 3."""

    candidate = hexlify(input_data)

    if not isinstance(candidate, str):
        candidate = candidate.decode('utf-8')

    return candidate
