import cocotb
import cocotb.triggers


async def pins_cycle(dut, *, rst_n=1, pin_in=0, write_out=0, write_oe=0, write_pin=0, write_value=0, side_write=0, side_pin=0, side_value=0):
    dut.clk.value = 0
    dut.rst_n.value = rst_n
    dut.pin_in.value = pin_in
    dut.write_out.value = write_out
    dut.write_oe.value = write_oe
    dut.write_pin.value = write_pin
    dut.write_value.value = write_value
    dut.side_write.value = side_write
    dut.side_pin.value = side_pin
    dut.side_value.value = side_value

    await cocotb.triggers.Timer(1, unit="ns")
    dut.clk.value = 1
    await cocotb.triggers.Timer(1, unit="ns")

    return int(dut.sampled_pins.value), int(dut.pin_out.value), int(dut.pin_oe.value)


@cocotb.test()
async def test_input_synchronisation(dut):
    await pins_cycle(dut, rst_n=0)

    for pin_in, expected in [(0xA5, 0), (0x5A, 0xA5), (0, 0x5A)]:
        sampled_pins, _, _ = await pins_cycle(dut, pin_in=pin_in)
        assert sampled_pins == expected, f"expected sampled pins {expected:#04x}, got {sampled_pins:#04x}"


@cocotb.test()
async def test_output_value_and_enable(dut):
    await pins_cycle(dut, rst_n=0)

    _, pin_out, pin_oe = await pins_cycle(dut, write_out=1, write_pin=3, write_value=1)
    assert (pin_out, pin_oe) == (0x08, 0), f"expected pin 3 high with drive disabled, got {pin_out:#04x}, {pin_oe:#04x}"

    _, pin_out, pin_oe = await pins_cycle(dut, write_oe=1, write_pin=3, write_value=1)
    assert (pin_out, pin_oe) == (0x08, 0x08), f"expected pin 3 to drive high, got {pin_out:#04x}, {pin_oe:#04x}"

    _, pin_out, pin_oe = await pins_cycle(dut, write_oe=1, write_pin=3, write_value=0)
    assert (pin_out, pin_oe) == (0x08, 0), f"expected pin 3 released with its value held, got {pin_out:#04x}, {pin_oe:#04x}"


@cocotb.test()
async def test_side_set(dut):
    await pins_cycle(dut, rst_n=0)

    _, pin_out, pin_oe = await pins_cycle(dut, write_out=1, write_pin=0, write_value=1, side_write=1, side_pin=7, side_value=1)
    assert pin_out == 0x81, f"expected both writes to take effect, got {pin_out:#04x}"
    assert pin_oe == 0, f"expected output enables to stay clear, got {pin_oe:#04x}"

    _, pin_out, _ = await pins_cycle(dut, write_out=1, write_pin=0, write_value=1, side_write=1, side_pin=0, side_value=0)
    assert pin_out == 0x80, f"expected side-set to clear pin 0 and leave pin 7 high, got {pin_out:#04x}"


@cocotb.test()
async def test_reset_releases_pins(dut):
    await pins_cycle(dut, rst_n=0)
    await pins_cycle(dut, pin_in=0xFF, write_out=1, write_pin=7, write_value=1)
    await pins_cycle(dut, pin_in=0xFF, write_oe=1, write_pin=7, write_value=1)

    actual = await pins_cycle(dut, rst_n=0, pin_in=0xFF)
    expected = (0, 0, 0)
    assert actual == expected, f"expected reset to clear sampled inputs, outputs and enables, got {actual}"

    actual = await pins_cycle(dut, pin_in=0xFF)
    assert actual == expected, f"expected reset to clear both synchroniser stages, got {actual}"
