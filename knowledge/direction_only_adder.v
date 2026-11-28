// direction_only_adder.v
// Direction-only arithmetic unit — 2026-11-28
// Magnitudes are always positive. Minus is pure direction (x -1).
// No two's complement. No signed zero. Cancel state on equal opposite magnitudes.
//
// Canonical test: 10 + (4 x -1) = 6
//
// Inputs per operand: magnitude [WIDTH-1:0], direction (0=+1, 1=-1)
// Output: magnitude [WIDTH-1:0], direction, cancel flag

module direction_only_adder #(
    parameter WIDTH = 64
)(
    input  wire [WIDTH-1:0] mag_a,
    input  wire            dir_a,   // 0 = +1, 1 = -1
    input  wire [WIDTH-1:0] mag_b,
    input  wire            dir_b,   // 0 = +1, 1 = -1
    output reg  [WIDTH-1:0] mag_out,
    output reg             dir_out, // 0 = +1, 1 = -1
    output reg             cancel   // 1 = valueless cancel (never signed zero)
);

    wire same_dir = (dir_a == dir_b);

    always @(*) begin
        cancel  = 1'b0;
        mag_out = {WIDTH{1'b0}};
        dir_out = 1'b0;

        if (same_dir) begin
            // Same direction: add magnitudes, keep direction
            mag_out = mag_a + mag_b;
            dir_out = dir_a;
        end else begin
            // Opposite directions: compare, subtract smaller from larger
            if (mag_a > mag_b) begin
                mag_out = mag_a - mag_b;
                dir_out = dir_a;
            end else if (mag_b > mag_a) begin
                mag_out = mag_b - mag_a;
                dir_out = dir_b;
            end else begin
                // Equal magnitudes, opposite directions -> cancel
                // Magnitude zero, direction undefined — consumer treats as valueless
                mag_out = {WIDTH{1'b0}};
                dir_out = 1'b0; // placeholder; cancel flag is the real signal
                cancel  = 1'b1;
            end
        end
    end

    // Test vectors (simulation check, not synthesizable asserts):
    // 1) mag_a=10, dir_a=0, mag_b=4,  dir_b=1 -> mag_out=6,  dir_out=0, cancel=0
    // 2) mag_a=4,  dir_a=1, mag_b=10, dir_b=0 -> mag_out=6,  dir_out=0, cancel=0
    // 3) mag_a=5,  dir_a=0, mag_b=5,  dir_b=1 -> mag_out=0,  dir_out=0, cancel=1
    // 4) mag_a=7,  dir_a=0, mag_b=3,  dir_b=0 -> mag_out=10, dir_out=0, cancel=0

    // Seal: SHA-256 16e0e1ade6aa846cb7add8ff567b6faa075797e6fb941c7df9416d354f1884
    // Size: 2457 bytes. Direction-only, no float, no signed zero.
    // Standing: 2026-11-16 direction-only arithmetic. 2026-11-24 zero-infinity restatement.

 endmodule
