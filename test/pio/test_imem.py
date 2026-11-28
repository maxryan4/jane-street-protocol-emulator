import cocotb
import cocotb.triggers


@cocotb.test()
async def test_host_write_and_independent_reads(dut):
    dut.clk.value = 0
    dut.host_write.value = 0
    dut.pc.value = 0

    words = [0x8000 | (slot << 8) | (15 - slot) for slot in range(16)]
    for slot, word in enumerate(words):
        dut.clk.value = 0
        dut.host_write.value = 1
        dut.host_addr.value = slot
        dut.host_wdata.value = word
        await cocotb.triggers.Timer(1, unit="ns")
        dut.clk.value = 1
        await cocotb.triggers.Timer(1, unit="ns")

    dut.host_write.value = 0
    dut.host_wdata.value = 0
    dut.clk.value = 0
    await cocotb.triggers.Timer(1, unit="ns")
    dut.clk.value = 1
    await cocotb.triggers.Timer(1, unit="ns")

    previous = words[15], words[0]
    for host_slot in range(16):
        fetch_slot = 15 - host_slot
        dut.clk.value = 0
        dut.host_addr.value = host_slot
        dut.pc.value = fetch_slot
        await cocotb.triggers.Timer(1, unit="ns")

        actual = int(dut.host_rdata.value), int(dut.instruction.value)
        assert actual == previous, f"expected both reads to hold before the rising edge, got {actual}"

        dut.clk.value = 1
        await cocotb.triggers.Timer(1, unit="ns")
        actual = int(dut.host_rdata.value), int(dut.instruction.value)
        expected = words[host_slot], words[fetch_slot]
        assert actual == expected, f"expected host slot {host_slot} and fetch slot {fetch_slot} to read {expected}, got {actual}"
        previous = expected
