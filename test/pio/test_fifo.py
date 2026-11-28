import cocotb
import cocotb.triggers


async def fifo_cycle(dut, *, rst_n=1, word=None, pop=0):
    dut.clk.value = 0
    dut.rst_n.value = rst_n
    dut.push.value = int(word is not None)
    dut.push_data.value = word if word is not None else 0
    dut.pop.value = pop
    await cocotb.triggers.Timer(1, unit="ns")

    data = int(dut.pop_data.value) if rst_n else None
    dut.clk.value = 1
    await cocotb.triggers.Timer(1, unit="ns")

    return data, int(dut.full.value), int(dut.empty.value)


@cocotb.test()
async def test_fifo_order_and_simultaneous_requests(dut):
    await fifo_cycle(dut, rst_n=0)

    for word, pop, expected in [
        (0x1234, 1, (0, 0, 0)),
        (0x5678, 1, (0x1234, 0, 0)),
        (0x9ABC, 0, (0x5678, 1, 0)),
        (0xFFFF, 1, (0x5678, 0, 0)),
        (None, 1, (0x9ABC, 0, 1)),
        (None, 1, (0, 0, 1)),
    ]:
        actual = await fifo_cycle(dut, word=word, pop=pop)
        assert actual == expected, f"for push {word} and pop {pop}, expected {expected}, got {actual}"

    await fifo_cycle(dut, word=0xFFFF)
    await fifo_cycle(dut, word=0xFFFE)
    actual = await fifo_cycle(dut, rst_n=0)
    assert actual == (None, 0, 1), f"expected reset to empty a full FIFO, got {actual}"
