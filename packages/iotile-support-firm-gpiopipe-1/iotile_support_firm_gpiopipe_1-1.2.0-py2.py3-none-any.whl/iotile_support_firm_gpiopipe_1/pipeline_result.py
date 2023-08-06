"""Data class for handling the configuration of Pipeline results."""

import struct
from iotile.core.exceptions import ArgumentError


class PipelineResult(object):
    """Representation of a pipeline result.

    Pipeline results allow combining the last value from one or more pipelines
    into a single field using bit masking and support automatically pushing
    those results on change to another tile.
    """

    CONFIG_SIZE = 15
    PIPELINE_SOURCES = 4
    ENABLED_BIT = (1 << 2)
    CONFIG_FORMAT = "<12sBBB"

    FIRST_UPDATE_BIT = (1 << 0)
    UPDATED_BIT = (1 << 1)
    CHANGED_BIT = (1 << 2)

    PUSH_SETTINGS = {
        0: 'never',
        1: 'on change',
        2: 'on update'
    }

    def __init__(self, index, sources, push_settings=None, state_flags=None, value=None):
        self.index = index
        self.sources = sources
        self.push_settings = push_settings

        self._value = value
        self._state_flags = state_flags

    @property
    def state(self):
        """The current state of the result.

        Returns:
            str
        """

        if self._state_flags is None:
            return "unknown"

        if self._state_flags & self.FIRST_UPDATE_BIT:
            return "nothing"

        if self._state_flags & self.CHANGED_BIT:
            return "changed"

        if self._state_flags & self.UPDATED_BIT:
            return "updated"

        return 'same'

    def get_value(self, default=None):
        """Get the value in the result with an optional default."""

        if self.state == 'nothing':
            return default

        return self._value

    def encode(self):
        """Encode this object into a binary configuration blob.

        This configuration blob is suitable for passing to
        PipelineResult.FromBinary and recovering the original settings.

        Returns:
            bytes
        """

        encoded_sources = b''.join(x.encode() for x in self.sources)
        if len(encoded_sources) < 12:
            encoded_sources += b'\0'*(12 - len(encoded_sources))

        stream, tile, flags = self.push_settings.encode()

        flags |= self.ENABLED_BIT
        return struct.pack(self.CONFIG_FORMAT, encoded_sources, stream, tile, flags)

    @classmethod
    def FromBinary(cls, index, binary_config, flags=None, value=None):
        """Create a PipelineResult from binary data.

        This method allows for deserializing the result of an inspect_result
        RPC call.

        Args:
            index (int): The result index
            binary_config (bytes): The raw binary data containing the
                configuration of the result object.
            flags (int): The packed flags from the result's state
            value (int): The last value stored in the result.

        Returns:
            PipelineResult: The decoded pipeline result or None if it was not enabled.
        """

        if len(binary_config) != cls.CONFIG_SIZE:
            raise ArgumentError("Binary config blob is the incorrect size, expected %d received %d" %
                                (cls.CONFIG_SIZE, len(binary_config)))

        sources, dest_stream, dest_tile, config_flags = struct.unpack(cls.CONFIG_FORMAT, binary_config)

        decoded_sources = []
        for i in range(0, cls.PIPELINE_SOURCES):
            bin_source = sources[3 * i:(3 * i) + 3]
            source = PipelineSource.FromBinary(bin_source)
            if source is not None:
                decoded_sources.append(source)

        push_condition = config_flags & 0b11
        enabled = bool(config_flags & (1 << 2))

        push_string = cls.PUSH_SETTINGS.get(push_condition)
        if push_string is None:
            raise ArgumentError("Invalid push configuration: unknown code %d" % push_condition)

        if not enabled:
            return None

        if push_condition == 'never':
            push_settings = ResultPushSettings()
        else:
            push_settings = ResultPushSettings(dest_tile, dest_stream, push_string)

        return PipelineResult(index, decoded_sources, push_settings, flags, value)

    @classmethod
    def FromString(cls, index, descriptor):
        """Parse a string descriptor for a PipelineResult.

        The format for the string is:
        bitmask [push to tile_address:stream [on (change|update)]][, letter: pipeline X:a-b]*

        The bitmask is a series of a letters that identify blocks of bits.
        The letters can be repeated, one per bit or there can be an integer N
        in base 10 before a letter which is equivalent to repeating that
        letter N times.  For example:

        aa28xbb, a: pipeline 1:0-2, b: pipeline 2:30-31

        This would specify a result where the first 2 bits are bits 0:2 from
        pipeline 1, followed by 28 0 bits followed by 2 bits from pipeline 2
        bits 30-31.

        The bitmask must always expand to exactly 32 bits to ensure that it
        was specified correctly.

        Args:
            index (int): The index of the result that you want to set.
            descriptor (str): The string descriptor containing the result.
        """

        bitmask, push_settings, sources = divide_result_descriptor(descriptor)

        bit_ranges = parse_bitmask(bitmask)
        parsed_sources = [list(parse_source(x).items())[0] for x in sources]
        source_map = {letter: source for letter, source in parsed_sources}
        if len(source_map) != len(sources):
            raise ArgumentError("Duplicate source letter in source descriptors", sources=sources)

        total_bits = 0
        ordered_sources = []

        for letter, count in bit_ranges:
            if letter == 'x':
                source = PipelineSource(None, count)
            elif letter not in source_map:
                raise ArgumentError("Bitmask referenced undefined source '%s'" % letter)
            else:
                source = source_map[letter]

            if source.length != count:
                raise ArgumentError("Mismatch between bitmask length '%d' and configured source: %s" % (count, source))

            total_bits += count
            ordered_sources.append(source)

        if total_bits != 32:
            raise ArgumentError("Bitmask did not have exactly 32 bits defined: %s" % bitmask)

        if len(push_settings) == 0:
            push = ResultPushSettings()
        else:
            push = ResultPushSettings.FromString(push_settings) 

        return PipelineResult(index, ordered_sources, push)

    def __eq__(self, other):
        if not isinstance(other, PipelineResult):
            return False

        if self.index != other.index:
            return False

        if self.push_settings != other.push_settings:
            return False

        if len(self.sources) != len(other.sources):
            return False

        if self._state_flags != other._state_flags or self._value != other._value:
            return False

        for source1, source2 in zip(self.sources, other.sources):
            if source1 != source2:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        representation, letters = create_bitmask(self.sources)

        if self.push_settings.enabled:
            representation += " {}".format(str(self.push_settings))

        pipeline_sources = (x for x in self.sources if x.pipeline is not None)
        source_string = ", ".join("{}: {}".format(letter, str(x)) for letter, x in zip(letters, pipeline_sources))
        if source_string != "":
            representation += ", {}".format(source_string)

        return representation


class ResultPushSettings(object):
    """Automatic push configuration.

    This class encapsulates the settings of whether and when a result should
    be automatically pushed to another tile.
    """

    ON_CHANGE = "on change"
    ON_CHANGE_ENC = 1

    ON_UPDATE = "on update"
    ON_UPDATE_ENC = 2

    NEVER = "never"

    PUSH_CHOICES = (ON_CHANGE, ON_UPDATE, NEVER)

    def __init__(self, dest_tile=None, dest_stream=None, condition="never"):

        if condition not in self.PUSH_CHOICES:
            raise ArgumentError("Invalid push condition: %s" % condition)

        self.enabled = condition != "never"
        self.when = condition

        if self.enabled:
            if dest_tile is None or dest_stream is None:
                raise ArgumentError("You must specify either a destination tile and a destination stream")

            if dest_tile < 8 or dest_tile >= 128:
                raise ArgumentError("The destination tile address must be in the range [8, 127], address=%d" % dest_tile)

            if dest_stream < 0 or dest_stream >= 0x100:
                raise ArgumentError("The destination stream must be in the range [0, 255], stream=%d" % dest_stream)

        self.dest_tile = dest_tile
        self.dest_stream = dest_stream

    def encode(self):
        """Encode this as 3 numbers.

        This will return the 3 1-byte numbers corresponding to the
        destination_stream, destination_tile and push condition.

        Returns:
            3-tuple of int: The destination stream, tile and condition
        """

        if self.enabled is False:
            return (0, 0, 0)

        if self.when == self.ON_CHANGE:
            encoded_condition = self.ON_CHANGE_ENC
        else:
            encoded_condition = self.ON_UPDATE_ENC

        return (self.dest_stream, self.dest_tile, encoded_condition)

    def __str__(self):
        if not self.enabled:
            return "never push"

        return "push to %d:0x%02x %s" % (self.dest_tile, self.dest_stream, self.when)

    def __eq__(self, other):
        if not isinstance(other, ResultPushSettings):
            return False

        return self.when == other.when and self.dest_tile == other.dest_tile and self.dest_stream == other.dest_stream

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def FromString(cls, descriptor):
        """Create push settings from a string descriptor.

        The format is:

        [push to] {tile: int}:{stream: int in hex} (on change|on update)

        Args:
            descriptor (str): The string descriptor to parse into a ResultPushSettings.

        Returns:
            ResultPushSettings:
        """

        descriptor = descriptor.strip()

        if descriptor.startswith('push to'):
            descriptor = descriptor[7:]

        if descriptor.endswith('on change'):
            push_type = 'on change'
            descriptor = descriptor[:-9]
        elif descriptor.endswith('on update'):
            push_type = 'on update'
            descriptor = descriptor[:-9]
        else:
            push_type = 'on update'

        if ':' not in descriptor:
            raise ArgumentError("Invalid tile:stream destination '%s', missing ':'" % descriptor)

        tile, _, stream = descriptor.partition(':')

        try:
            tile = int(tile)
        except ValueError:
            raise ArgumentError("Could not parse destination tile as a decimal int: %s" % tile)

        try:
            stream = int(stream, 0)
        except ValueError:
            raise ArgumentError("Could not parse destination stream as an int: %s" % stream)

        return ResultPushSettings(tile, stream, push_type)


class PipelineSource(object):
    """A configured result input that pulls specific bits from a given pipeline.

    This allows you to assemble a PipelineResult from one or more individual
    pipelines taking X bits from each one and swizzling them together to
    produce a single value.

    This object basically says, take ``length`` bits from pipeline X starting
    at bit ``start_bit`` and place them into this PipelineResult.

    Args:
        pipeline (int): The index of the pipeline that we want to pull data from.
            If this is None, then the source will load in 0 bits instead, which
            can be useful as a placeholder.
        length (int): The number of bits that this source should contribute.
        start_bit (int): The bit of the pipeline result to start with.  This is
            ignored when pipeline=None since there is no source pipeline result
            in that case.
        stage (int): The pipeline stage to attach to.
    """

    MAX_STAGE = 7
    BINARY_SIZE = 3
    ENABLED_BIT = (1 << 7)
    CLEAR_BIT = (1 << 5)

    def __init__(self, pipeline, length, start_bit=0, stage=None):
        if pipeline is None and (start_bit != 0 or stage is not None):
            raise ArgumentError("You cannot specify a start bit or stage if pipeline=None", start_bit=start_bit, stage=stage)

        if pipeline is not None and stage is None:
            stage = self.MAX_STAGE

        if length <= 0 or start_bit < 0:
            raise ArgumentError("Invalid start bit that is negative or length that is not positive", length=length, start_bit=start_bit)

        if (length + start_bit) > 32:
            raise ArgumentError("Source specification would exceed the size of a 32-bit field", length=length, start_bit=start_bit)

        if pipeline is not None and (stage < 0 or stage >= 16):
            raise ArgumentError("Invalid stage %d for pipeline %d, must be in [0, 15]" % (stage, pipeline))

        self.pipeline = pipeline
        self.length = length
        self.start_bit = start_bit
        self.stage = stage


    def encode(self):
        """Encode this source descriptor as a binary blob.

        Returns:
            bytes
        """

        encoded_length = self.length - 1
        assert 0 <= encoded_length < 32

        if self.pipeline is None:
            pipeline_byte = 0
            stage_byte = 0
        else:
            pipeline_byte = self.pipeline & 0b111 | ((self.start_bit & 0b11111) << 3)
            stage_byte = self.stage & 0b1111

        length_flags_byte = (encoded_length & 0b11111)

        if self.pipeline is None:
            length_flags_byte |= self.CLEAR_BIT

        length_flags_byte |= self.ENABLED_BIT

        return struct.pack("<BBB", pipeline_byte, length_flags_byte, stage_byte)

    @classmethod
    def FromBinary(cls, binary_source):
        """Create a PipelineSource from binary data.

        This method allows for deserializing the binary description of a
        source received from the tile.  If the binary source descriptor
        indicates that this source is disabled then None will be returned.

        Args:
            binary_source (bytes): The binary source descriptor received
                from the tile.

        Returns:
            PipelineSource: The decoded PipelineSource or None

            None will be returned if the pipeline source does not have its
            enabled bit set indicating that it is not describing a valid
            PipelineSource.
        """

        if len(binary_source) != cls.BINARY_SIZE:
            raise ArgumentError("Binary source blog is the incorrect size, expected %d received %d" %
                                (cls.BINARY_SIZE, len(binary_source)))

        pipeline_byte, length_flags_byte, stage_byte = struct.unpack("<BBB", binary_source)

        if not bool(length_flags_byte & cls.ENABLED_BIT):
            return None

        pipeline = pipeline_byte & (0b111)
        start_bit = (pipeline_byte >> 3) & (0b11111)
        length = length_flags_byte & 0b11111
        clear = bool(length_flags_byte & cls.CLEAR_BIT)
        stage = stage_byte & 0b1111

        # We encode (length - 1) to fit it into 5 bits while supporting the value 32
        length += 1

        if clear:
            pipeline = None
            start_bit = 0
            stage = None

        return PipelineSource(pipeline, length, start_bit=start_bit, stage=stage)

    def __str__(self):
        if self.pipeline is None:
            return "{} zero bits".format(self.length)

        return "pipeline {}.{}[{}-{}]".format(self.pipeline, self.stage, self.start_bit, self.start_bit + self.length)

    def __repr__(self):
        return "PipelineSource (source=%s:%s, start=%d, length=%d)" % (self.pipeline, self.stage, self.start_bit, self.length)

    def __eq__(self, other):
        if not isinstance(other, PipelineSource):
            return False

        return self.pipeline == other.pipeline and self.start_bit == other.start_bit and self.length == other.length and self.stage == other.stage

    def __ne__(self, other):
        return not self.__eq__(other)


def divide_result_descriptor(descriptor):
    """Divide a result descriptor into its three logical parts.

    The format for the string is:
        bitmask [push to tile_address:stream [on (change|update)]][, letter: pipeline X[a:b]]*

    Args:
        descriptor (str): The string result descriptor.

    Returns:
        str, str, list(str): The bitmask, push settings and any pipeline sources.
    """

    parts = descriptor.split(',')

    sources = parts[1:]
    result_desc = parts[0]

    if 'push to' in result_desc:
        bitmask, _, push_settings = result_desc.partition('push to')
    else:
        bitmask = result_desc
        push_settings = ""

    bitmask = bitmask.strip()
    push_settings = push_settings.strip()
    sources = [x.strip() for x in sources]

    return bitmask, push_settings, sources


def parse_source(source):
    """Parse a string pipeline source.

    Pipeline sources are described by a string descriptor like:
    X: pipeline N[a-b]

    where:
    - X is an ascii letter
    - N is a decimal number
    - a nd b are decimal numbers

    This says that letter X should be replaced with bits a-b of the result
    from pipeline N.

    Returns:
        {str: PipelineSource}: The parsed source and it's letter identifier.
    """

    letter, _, pipeline = source.partition(':')

    letter = letter.strip()
    pipeline = pipeline.strip()

    if len(letter) != 1 or not letter.isalpha():
        raise ArgumentError("Error parsing pipeline source descriptor '%s'" % source)

    if not pipeline.startswith('pipeline '):
        raise ArgumentError("Error parsing pipeline source descriptor '%s'" % source)

    pipeline = pipeline[9:]
    pipeline_index, _, bit_range = pipeline.partition('[')

    if len(bit_range) == 0 or bit_range[-1] != ']':
        raise ArgumentError("Could not interpret bit range specifier in pipeline: '%s" % source)

    bit_range = bit_range[:-1].strip()
    pipeline_index = pipeline_index.strip()

    stage = PipelineSource.MAX_STAGE
    if '.' in pipeline_index:
        pipeline_index, _, stage = pipeline_index.partition('.')

    try:
        pipeline_index = int(pipeline_index)
        stage = int(stage)
    except ValueError:
        raise ArgumentError("Could not interpret pipeline index '%s' or stage '%s' as a decimal integer" % (pipeline_index, stage))

    if '-' not in bit_range:
        raise ArgumentError("Could not interpret bit range '%s', missing -" % bit_range)

    start_bit, _, end_bit = bit_range.partition('-')
    start_bit = start_bit.strip()
    end_bit = end_bit.strip()

    try:
        start_bit = int(start_bit)
        end_bit = int(end_bit)
    except ValueError:
        raise ArgumentError("Could not parse bit range as decimal integers [%s-%s]" % (start_bit, end_bit))

    if end_bit <= start_bit:
        raise ArgumentError("bit range invalid, end bit <= start bit: source=%s" % source)

    return {letter: PipelineSource(pipeline_index, end_bit - start_bit, start_bit, stage=stage)}


def convert_bitmask(bitmask):
    """Replace numerical placeholders with repeated characters."""

    converted_bitmask = ""

    number = ""
    for char in bitmask:
        if char.isdigit():
            number += char
        elif number != "":
            try:
                number = int(number)
            except ValueError:
                raise ArgumentError("Could not understand embedded repeat count '%s' in bitmask '%s'" % (number, bitmask))

            converted_bitmask += (char * number)
            number = ""
        else:
            converted_bitmask += char

    if number != "":
        raise ArgumentError("bitmask '%s' embedded a repeat count ('%s') without being followed by a character" % (bitmask, number))

    return converted_bitmask


def parse_bitmask(bitmask):
    """Parse a bitmask field."""

    bitmask = convert_bitmask(bitmask)

    parsed = []

    count = 0
    last_char = None

    for char in bitmask:
        if not char.isalpha():
            raise ArgumentError("Non-ascii character '%s' in bitmask: %s" % (char, bitmask))

        if last_char is not None and char != last_char:
            parsed.append((last_char, count))
            count = 0
            last_char = None

        last_char = char
        count += 1

    if last_char is not None:
        parsed.append((last_char, count))

    return parsed


def create_bitmask(sources):
    """Create a bitmask from a list of sources."""

    id_list = "abcd"
    id_index = 0

    bitmask = ""
    letters = ""

    for source in sources:
        if source.pipeline is None:
            portion = (source.length, "x")
        elif id_index >= len(id_list):
            raise ArgumentError("Too many non-empty sources (only 4 supported), length=%d" % len(sources))
        else:
            portion = (source.length, id_list[id_index])
            letters += portion[1]
            id_index += 1

        if portion[0] == 1:
            bitmask += portion[1]
        else:
            bitmask += "{}{}".format(*portion)

    return bitmask, letters
