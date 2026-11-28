module clkdiv #(
    parameter int WIDTH = 16
) (
    input logic clk,
    input logic rst_n,
    input logic run,
    input logic [WIDTH-1:0] divider,
    output logic tick
);

  logic [WIDTH-1:0] count;

  // assert tick before its sampling edge so divider zero ticks every cycle
  assign tick = rst_n && run && (count == divider);

  always_ff @(posedge clk) begin
    if (!rst_n || !run || tick) begin
      count <= '0;
    end

    else begin
      count <= count + 1'b1;
    end
  end

endmodule
