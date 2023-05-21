$fa = 1;
$fs = 0.4;

function mm(mil) = mil * 0.0254;
err = 0.3;
inf = 1000;
wall = 1.5;
hole_r = mm(550) + err;
hole_x = mm(1500);
hole_y = mm(950);
case_r = mm(850) + err;
case_skirt = 5;
case_raise = mm(600);
case_z = mm(2800);
mcu_err = 1;
mcu_x = mm(1000) + mcu_err;
mcu_y = mm(450) + mcu_err;
mcu_r = mm(100) + mcu_err;
port_x = mm(500);
port_y = mm(300);

module cylinder4 (r1, r2, h) {
    translate([hole_x, hole_y, 0])
        cylinder(r1=r1, r2=r2, h=h, center=true);
    translate([-hole_x, hole_y, 0])
        cylinder(r1=r1, r2=r2, h=h, center=true);
    translate([hole_x, -hole_y, 0])
        cylinder(r1=r1, r2=r2, h=h, center=true);
    translate([-hole_x, -hole_y, 0])
        cylinder(r1=r1, r2=r2, h=h, center=true);
}

module case (r1, r2) {
    translate([0, 0, - 0.5 * case_z])
        cylinder4(r1, r2, case_z);
    translate([0, 0, - 0.5 * case_z])
    cube([hole_x * 2 + r2 * 2, hole_y * 2, case_z], center=true);
    translate([0, 0, - 0.5 * case_z])
    cube([hole_x * 2, hole_y * 2 + r2 * 2, case_z], center=true);
}


module SmoothXYCube(size, smooth_rad) {
    //https://github.com/rcolyer/smooth-prim/blob/master/smooth_prim.scad#LL147C1-L173C2
    $fa = ($fa >= 12) ? 1 : $fa;
    $fs = ($fs >= 2) ? 0.4 : $fs;

    size = is_num(size) ? [size, size, size] : size;

    scalex = (smooth_rad < size[0]/2) ? 1 : size[0]/(2*smooth_rad);
    scaley = (smooth_rad < size[1]/2) ? 1 : size[1]/(2*smooth_rad);
    smoothx = smooth_rad * scalex;
    smoothy = smooth_rad * scaley;

    linear_extrude(size[2]) hull() {
        translate([smoothx, smoothy])
        scale([scalex, scaley])
            circle(r=smooth_rad);
        translate([size[0]-smoothx, smoothy])
        scale([scalex, scaley])
            circle(r=smooth_rad);
        translate([smoothx, size[1]-smoothy])
        scale([scalex, scaley])
            circle(r=smooth_rad);
        translate([size[0]-smoothx, size[1]-smoothy])
        scale([scalex, scaley])
            circle(r=smooth_rad);
    }
}

rotate([0, 180, 0])
difference () {
    union () {
        difference() {
            case(
                case_r + wall + case_skirt,
                case_r + wall
            );
            translate([0, 0, -wall])
                case(
                    case_r,
                    case_r
                );
        }
        translate([0, 0, - 0.5 * case_raise])
            cylinder4(
                hole_r + wall,
                hole_r + wall,
                case_raise);
    }
    translate([0, 0, - 0.5 * case_raise])
        cylinder4(
            hole_r,
            hole_r,
            inf);
    translate([-mcu_x, -mcu_y, - 0.5 * inf ])
        SmoothXYCube(size = [
            mcu_x * 2,
            mcu_y * 2,
            inf
        ], smooth_rad = mcu_r);
    translate([0.5 * inf, 0, -port_y / 2 - wall])
    rotate([0, 90, 0])
        cube([port_y, port_x, inf], center=true);

    translate([
        0.5 * inf,
        0,
        -case_raise - 1.6 - sqrt(0.5) * 5 ])
    rotate([0, 90, 0])
    rotate([0, 0, 45])
        cube([5, 5, inf], center=true);
}

