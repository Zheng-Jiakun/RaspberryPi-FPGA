module top (
	input clk,
	input rst_n,

	output [3:0] led,

	input pi_clk,
	input pi_rw,
	input [5:0] pi_addr,
	inout [7:0] pi_data
);

	reg [7:0] fpga_reg [0:63];
	reg [7:0] pi_data_buffer;

	integer i;
	always@(posedge pi_clk or negedge rst_n) begin
		if (!rst_n) begin
			for (i = 0; i < 64; i = i + 1) begin
				fpga_reg[i] <= 8'h00;
			end
		end
		else if (!pi_rw) begin	// pi_rw = 0 -> write
			fpga_reg[pi_addr] <= pi_data;
		end
	end

	always@(posedge pi_clk or negedge rst_n) begin
		if (!rst_n) begin
			pi_data_buffer <= 8'h00;
		end
		else if (pi_rw) begin	// pi_rw = 1 -> read
			pi_data_buffer <= fpga_reg[pi_addr];
		end
	end

	assign pi_data = pi_rw ? pi_data_buffer : 8'bz;

	assign led[3:0] = ~fpga_reg[0][3:0];


endmodule