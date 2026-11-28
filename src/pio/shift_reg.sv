module shift_reg #(
    parameter int WIDTH = 16
) (
    input logic clk,
    input logic rst_n,
    input logic start,

    input logic shift_in,
    input logic shift_out,
    input logic push_rx,
    input logic pull_tx,

    input logic pin_bit,
    output logic serial_out_bit,
    input logic [WIDTH-1:0] tx_data,
    output logic [WIDTH-1:0] rx_data
);

  logic [WIDTH-1:0] isr;
  logic [WIDTH-1:0] osr;

  assign serial_out_bit = osr[WIDTH-1];
  assign rx_data = isr;

  always_ff @(posedge clk) begin
    if (!rst_n || start) begin
      isr <= 0;
      osr <= 0;
    end

    else begin
      if (push_rx) begin
        isr <= 0;
      end

      else if (shift_in) begin
        isr <= (isr << 1) | WIDTH'(pin_bit);
      end

      if (pull_tx) begin
        osr <= tx_data;
      end

      else if (shift_out) begin
        osr <= osr << 1;
      end
    end
  end

endmodule
