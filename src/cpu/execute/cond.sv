// COND: decides whether a conditional jump is taken, and flags a return.

module cond (
  input  logic       FLAGN,     // Negative
  input  logic       FLAGZ,     // Zero
  input  logic       FLAGC,     // Carry
  input  logic       FLAGV,     // oVerflow (not used)
  input  logic [3:0] JMPCOND,   // MSB being bit 3
  output logic       JUMP,      // Jump
  output logic       RET        // Return
);

  logic mux1_out;   
  logic [2:0] sel;
  assign sel = JMPCOND[3:1];

  always_comb begin
    case (sel)
      3'b001:  mux1_out = FLAGZ;   // select 1: Z
      3'b010:  mux1_out = FLAGC;   // select 2: C
      3'b011:  mux1_out = FLAGN;   // select 3: N
      default: mux1_out = 1'b1;
    endcase
  end

  assign JUMP = JMPCOND[0] ^ mux1_out;

  assign RET  = JMPCOND[3:0] == 4'b1111;

endmodule