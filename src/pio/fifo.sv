module fifo #(
    parameter int WIDTH = 16
) (
    input logic clk,
    input logic rst_n,

    input logic push,
    input logic [WIDTH-1:0] push_data,
    output logic full,

    input logic pop,
    output logic [WIDTH-1:0] pop_data,
    output logic empty
);

  logic [WIDTH-1:0] words [0:1];
  logic read_slot;
  logic write_slot;
  logic [1:0] count;
  logic push_word;
  logic pop_word;

  assign full = count == 2'd2;
  assign empty = count == 2'd0;
  assign pop_data = empty ? '0 : words[read_slot];

  // pre-edge flags decide which requests can complete
  assign push_word = push && !full;
  assign pop_word = pop && !empty;

  always_ff @(posedge clk) begin
    if (!rst_n) begin
      read_slot <= 1'b0;
      write_slot <= 1'b0;
      count <= 2'd0;
    end

    else begin
      if (push_word) begin
        words[write_slot] <= push_data;
        write_slot <= !write_slot;
      end

      if (pop_word) begin
        read_slot <= !read_slot;
      end

      if (push_word && !pop_word) begin
        count <= count + 2'd1;
      end

      else if (pop_word && !push_word) begin
        count <= count - 2'd1;
      end
    end
  end

endmodule
