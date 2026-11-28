module clkdiv (
    input wire clk,
    input wire rst_n,
    input wire run,
    input wire [15:0] divider,
    output wire tick
);

  logic [15:0] count;

  // assert tick before its sampling edge so divider zero ticks every cycle
  assign tick = rst_n && run && (count == divider);

  always_ff @(posedge clk) begin
    if (!rst_n || !run || tick) begin
      count <= 16'd0;
    end

    else begin
      count <= count + 16'd1;
    end
  end

endmodule
