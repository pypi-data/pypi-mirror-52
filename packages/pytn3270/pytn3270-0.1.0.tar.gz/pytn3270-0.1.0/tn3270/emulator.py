"""
tn3270.emulator
~~~~~~~~~~~~~~~
"""

from itertools import chain
import logging

from .datastream import Command, Order, AID, parse_outbound_message, \
                        format_inbound_read_buffer_message, \
                        format_inbound_read_modified_message

class Cell:
    """A display cell."""

class AttributeCell(Cell):
    """A attribute display cell."""

    def __init__(self, attribute):
        self.attribute = attribute

class CharacterCell(Cell):
    """A character display cell."""

    def __init__(self, byte):
        self.byte = byte

class OperatorError(Exception):
    """Operator error."""

class ProtectedCellOperatorError(OperatorError):
    """Protected cell error."""

class Emulator:
    """TN3270 emulator."""

    def __init__(self, stream, rows, columns):
        self.logger = logging.getLogger(__name__)

        # TODO: Validate that stream has read() and write() methods.
        self.stream = stream
        self.rows = rows
        self.columns = columns

        self.cells = [CharacterCell(0x00) for index in range(self.rows * self.columns)]
        self.address = 0
        self.cursor_address = 0
        self.current_aid = AID.NONE
        self.keyboard_locked = True

    def update(self, **kwargs):
        """Read a outbound message and execute command."""
        bytes_ = self.stream.read(**kwargs)

        if bytes_ is None:
            return False

        (command, *options) = parse_outbound_message(bytes_)

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug('Update')
            self.logger.debug(f'\tData    = {bytes_}')
            self.logger.debug(f'\tCommand = {command}')

        if command == Command.W:
            self._write(*options)
        elif command == Command.RB:
            self._read_buffer()
        elif command == Command.NOP:
            pass
        elif command == Command.EW:
            self._erase()
            self._write(*options)
        elif command == Command.RM:
            self._read_modified()
        elif command == Command.EWA:
            raise NotImplementedError('EWA command is not supported')
        elif command == Command.RMA:
            self._read_modified(all_=True)
        elif command == Command.EAU:
            self._erase_all_unprotected()
        elif command == Command.WSF:
            raise NotImplementedError('WSF command is not supported')

        return True

    def aid(self, aid):
        """AID key."""
        self.current_aid = aid
        self.keyboard_locked = True

        self._read_modified()

    def tab(self, direction=1):
        """Tab or backtab key."""
        address = self._calculate_tab_address(self.cursor_address, direction)

        if address is not None:
            self.cursor_address = address

    def newline(self):
        """Move to the next line or the subsequent unprotected field."""
        current_row = self.cursor_address // self.columns

        address = self._wrap_address((current_row + 1) * self.columns)

        (attribute, attribute_address) = self.find_attribute(address)

        if attribute is not None and not attribute.protected and attribute_address != address:
            self.cursor_address = address
            return

        address = self._calculate_tab_address(address, direction=1)

        if address is not None:
            self.cursor_address = address

    def home(self):
        """Home key."""
        addresses = self._get_addresses(0, (self.rows * self.columns) - 1)

        address = next((address for address in addresses
                        if isinstance(self.cells[address], AttributeCell)
                        and not self.cells[address].attribute.protected), None)

        if address is not None:
            self.cursor_address = self._wrap_address(address + 1)

    def cursor_up(self):
        """Cursor up key."""
        self.cursor_address = self._wrap_address(self.cursor_address - self.columns)

    def cursor_down(self):
        """Cursor down key."""
        self.cursor_address = self._wrap_address(self.cursor_address + self.columns)

    def cursor_left(self):
        """Cursor left key."""
        self.cursor_address = self._wrap_address(self.cursor_address - 1)

    def cursor_right(self):
        """Cursor right key."""
        self.cursor_address = self._wrap_address(self.cursor_address + 1)

    def input(self, byte):
        """Single character input."""
        if isinstance(self.cells[self.cursor_address], AttributeCell):
            raise ProtectedCellOperatorError

        (attribute, _) = self.find_attribute(self.cursor_address)

        if attribute is None or attribute.protected:
            raise ProtectedCellOperatorError

        # TODO: Implement numeric field validation.

        cell = self.cells[self.cursor_address]

        cell.byte = byte

        attribute.modified = True

        self.cursor_address = self._wrap_address(self.cursor_address + 1)

        # TODO: Is this correct - does this only happen if skip?
        if isinstance(self.cells[self.cursor_address], AttributeCell):
            skip = self.cells[self.cursor_address].attribute.skip

            addresses = self._get_addresses(self.cursor_address,
                                            self._wrap_address(self.cursor_address - 1))

            address = next((address for address in addresses
                            if isinstance(self.cells[address], AttributeCell)
                            and (not skip or (skip and not self.cells[address].attribute.protected))), None)

            if address is not None:
                self.cursor_address = self._wrap_address(address + 1)

    def backspace(self):
        """Backspace key."""
        if isinstance(self.cells[self.cursor_address], AttributeCell):
            raise ProtectedCellOperatorError

        (start_address, end_address, attribute) = self.get_field(self.cursor_address)

        if self.cursor_address == start_address:
            return

        self._shift_left(self._wrap_address(self.cursor_address - 1), end_address)

        attribute.modified = True

        self.cursor_address = self._wrap_address(self.cursor_address - 1)

    def delete(self):
        """Delete key."""
        if isinstance(self.cells[self.cursor_address], AttributeCell):
            raise ProtectedCellOperatorError

        (_, end_address, attribute) = self.get_field(self.cursor_address)

        self._shift_left(self.cursor_address, end_address)

        attribute.modified = True

    def get_bytes(self, start_address, end_address):
        """Get character cell bytes."""
        addresses = self._get_addresses(start_address, end_address)

        return bytes([self.cells[address].byte if isinstance(self.cells[address], CharacterCell) else 0x00 for address in addresses])

    def get_field(self, address):
        """Get the unprotected field containing the address."""
        (attribute, start_attribute_address) = self.find_attribute(address)

        if attribute is None or attribute.protected:
            raise ProtectedCellOperatorError

        addresses = self._get_addresses(address, self._wrap_address(address - 1))

        # TODO: Is this predicate correct?
        end_attribute_address = next((address for address in addresses
                                      if isinstance(self.cells[address], AttributeCell)),
                                     None)

        start_address = self._wrap_address(start_attribute_address + 1)

        if end_attribute_address is not None:
            end_address = self._wrap_address(end_attribute_address - 1)
        else:
            end_address = self._wrap_address(start_attribute_address - 1)

        return (start_address, end_address, attribute)

    def get_fields(self):
        """Get all unprotected fields."""
        fields = []

        for address in range(0, self.rows * self.columns):
            cell = self.cells[address]

            if isinstance(cell, AttributeCell) and not cell.attribute.protected:
                field = self.get_field(self._wrap_address(address + 1))

                fields.append(field)

        return fields

    def find_attribute(self, address):
        """Find the applicable attribute for the address."""
        for address in self._get_addresses(address, self._wrap_address(address + 1),
                                           direction=-1):
            cell = self.cells[address]

            if isinstance(cell, AttributeCell):
                return (cell.attribute, address)

        return (None, None)

    def _erase(self):
        self.logger.debug('Erase')

        self.cells = [CharacterCell(0x00) for index in range(self.rows * self.columns)]

        self.address = 0
        self.cursor_address = 0

    def _erase_all_unprotected(self):
        self.logger.debug('Erase All Unprotected')

        for (start_address, end_address, attribute) in self.get_fields():
            for address in range(start_address, end_address + 1):
                self.cells[address] = CharacterCell(0x00)

            attribute.modified = False

        self.current_aid = AID.NONE
        self.keyboard_locked = False

        # TODO: Repositions the cursor to the first character location, after the field
        # attribute, in the first unprotected field of the partition's character buffer.

    def _write(self, wcc, orders):
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug('Write')
            self.logger.debug(f'\tWCC = {wcc}')

        if wcc.reset_modified:
            for cell in self.cells:
                if isinstance(cell, AttributeCell):
                    cell.attribute.modified = False

        for (order, data) in orders:
            if self.logger.isEnabledFor(logging.DEBUG):
                if order is None:
                    self.logger.debug(f'\t{data}')
                else:
                    self.logger.debug(f'\t{order}')
                    self.logger.debug(f'\t\tParameters = {data}')

            if order == Order.PT:
                # TODO: PT is more complex to implement that simply duplicating the
                # behavior of tab() - how it behaves differs based on what command it
                # follows.
                raise NotImplementedError('PT order is not supported')
            elif order == Order.GE:
                raise NotImplementedError('GE order is not supported')
            elif order == Order.SBA:
                self.address = data[0]
            elif order == Order.EUA:
                unprotected_addresses = set()

                for (start_address, end_address, _) in self.get_fields():
                    unprotected_addresses.update(range(start_address, end_address + 1))

                stop_address = data[0]

                if self.address == stop_address:
                    addresses = range(0, self.rows * self.columns)
                else:
                    addresses = self._get_addresses(self.address,
                                                    self._wrap_address(stop_address - 1))

                for address in unprotected_addresses.intersection(addresses):
                    self.cells[address] = CharacterCell(0x00)

                self.address = stop_address
            elif order == Order.IC:
                self.cursor_address = self.address
            elif order == Order.SF:
                self.cells[self.address] = AttributeCell(data[0])

                self.address += 1
            elif order == Order.SA:
                raise NotImplementedError('SA order is not supported')
            elif order == Order.SFE:
                raise NotImplementedError('SFE order is not supported')
            elif order == Order.MF:
                raise NotImplementedError('MF order is not supported')
            elif order == Order.RA:
                (stop_address, byte) = data

                if self.address == stop_address:
                    addresses = range(0, self.rows * self.columns)
                else:
                    addresses = self._get_addresses(self.address,
                                                    self._wrap_address(stop_address - 1))

                for address in addresses:
                    self.cells[address] = CharacterCell(byte)

                self.address = stop_address
            elif order is None:
                for byte in data:
                    self.cells[self.address] = CharacterCell(byte)

                    self.address += 1

        if wcc.unlock_keyboard:
            self.current_aid = AID.NONE
            self.keyboard_locked = False

    def _read_buffer(self):
        orders = []

        data = bytearray()

        for cell in self.cells:
            if isinstance(cell, AttributeCell):
                if data:
                    orders.append((None, data))

                    data = bytearray()

                orders.append((Order.SF, [cell.attribute]))
            elif isinstance(cell, CharacterCell):
                data.append(cell.byte)

        if data:
            orders.append((None, data))

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug('Read Buffer')
            self.logger.debug(f'\tAID    = {self.current_aid}')

        bytes_ = format_inbound_read_buffer_message(self.current_aid, self.cursor_address, orders)

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(f'\tData   = {bytes_}')

        self.stream.write(bytes_)

    def _read_modified(self, all_=False):
        modified_field_ranges = [(start_address, end_address) for (start_address, end_address, attribute) in self.get_fields() if attribute.modified]

        fields = [(start_address, self.get_bytes(start_address, end_address)) for (start_address, end_address) in modified_field_ranges]

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug('Read Modified')
            self.logger.debug(f'\tAID    = {self.current_aid}')
            self.logger.debug(f'\tFields = {fields}')
            self.logger.debug(f'\tAll    = {all_}')

        bytes_ = format_inbound_read_modified_message(self.current_aid, self.cursor_address, fields, all_)

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(f'\tData   = {bytes_}')

        self.stream.write(bytes_)

    def _get_addresses(self, start_address, end_address, direction=1):
        if direction < 0:
            if end_address > start_address:
                return chain(reversed(range(0, start_address + 1)),
                             reversed(range(end_address, self.rows * self.columns)))

            return reversed(range(end_address, start_address + 1))

        if end_address < start_address:
            return chain(range(start_address, self.rows * self.columns),
                         range(0, end_address + 1))

        return range(start_address, end_address + 1)

    def _wrap_address(self, address):
        if address < 0 or address >= (self.rows * self.columns):
            return address % (self.rows * self.columns)

        return address

    def _calculate_tab_address(self, address, direction):
        if direction < 0:
            if address > 0 and isinstance(self.cells[address - 1], AttributeCell):
                address -= 1

            start_address = self._wrap_address(address - 1)
            end_address = self._wrap_address(address)
        else:
            start_address = self._wrap_address(address)
            end_address = self._wrap_address(address - 1)

        addresses = self._get_addresses(start_address, end_address, direction)

        address = next((address for address in addresses
                        if isinstance(self.cells[address], AttributeCell)
                        and not self.cells[address].attribute.protected), None)

        if address is None:
            return None

        return self._wrap_address(address + 1)

    def _shift_left(self, start_address, end_address):
        addresses = self._get_addresses(start_address, end_address)

        for (left_address, right_address) in zip(addresses, addresses[1:]):
            self.cells[left_address].byte = self.cells[right_address].byte

        self.cells[end_address].byte = 0x00
