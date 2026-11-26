// instruction decoding and operand selection
module decode(
    input  logic [15:0] INS,
    output logic OP2SEL, AD1SEL, WEN1, PCWRITE, EXT, MEMLDR, MEMSTR,
    output logic [2:0] A, B, C, ALUOPC,
    output logic [3:0] SCNT,
    output logic [1:0] SHIFTOPC,
    output logic [15:0] IMMS8, IMMS5
);

    logic data, alu_arith, shift, cmp;

    assign data = ~INS[15];
    assign ALUOPC = INS[14:12];
    assign shift = data & (ALUOPC == 3'd7);
    assign cmp = data & (ALUOPC == 3'd6);
    assign alu_arith = data & (ALUOPC >= 3'd1) & (ALUOPC <= 3'd5);

    assign PCWRITE = (INS[15:8] == 8'b11001110);
    assign MEMLDR = (INS[15:13] == 3'd4);
    assign MEMSTR = (INS[15:13] == 3'd5);
    assign OP2SEL = INS[8] & ~shift;
    assign AD1SEL = INS[8] | ~alu_arith;
    assign WEN1 = (data & ~cmp) | PCWRITE | MEMLDR;
    assign EXT = (INS[15:8] == 8'd0);
    assign A = INS[11:9];
    assign B = INS[7:5];
    assign C = INS[4:2];
    assign SCNT = INS[3:0];
    assign SHIFTOPC = {INS[8], INS[4]};
    assign IMMS8 = {{8{INS[7]}},  INS[7:0]};
    assign IMMS5 = {{11{INS[4]}}, INS[4:0]};

endmodule
