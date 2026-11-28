module imem #(
    parameter int WIDTH = 16
) (
    input logic clk,

    input logic host_write,
    input logic [3:0] host_addr,
    input logic [WIDTH-1:0] host_wdata,
    output logic [WIDTH-1:0] host_rdata,

    input logic [3:0] pc,
    output logic [WIDTH-1:0] instruction
);

  logic [WIDTH-1:0] words [0:15];

  always_ff @(posedge clk) begin
    instruction <= words[pc];

    if (host_write) begin
      words[host_addr] <= host_wdata;
    end

    else begin
      host_rdata <= words[host_addr];
    end
  end

endmodule
