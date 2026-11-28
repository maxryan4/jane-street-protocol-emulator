module pins (
    input logic clk,
    input logic rst_n,

    // raw gpio input
    input logic [7:0] pin_in,

    // synchronised input for pio instructions
    output logic [7:0] sampled_pins,

    // gpio drive values and enables
    output logic [7:0] pin_out,
    output logic [7:0] pin_oe,

    // pin writes from set and out instructions
    input logic write_out,
    input logic write_oe,
    input logic [2:0] write_pin,
    input logic write_value,

    // side-set write on an instruction tick
    input logic side_write,
    input logic [2:0] side_pin,
    input logic side_value
);

  logic [7:0] pin_in_sync_stage;

  always_ff @(posedge clk) begin
    if (!rst_n) begin
      pin_in_sync_stage <= 8'b0;
      sampled_pins <= 8'b0;
      pin_out <= 8'b0;
      pin_oe <= 8'b0;
    end

    else begin
      pin_in_sync_stage <= pin_in;
      sampled_pins <= pin_in_sync_stage;

      if (write_out) begin
        pin_out[write_pin] <= write_value;
      end

      if (write_oe) begin
        pin_oe[write_pin] <= write_value;
      end

      // side-set takes priority when both writes target one pin
      if (side_write) begin
        pin_out[side_pin] <= side_value;
      end
    end
  end

endmodule
