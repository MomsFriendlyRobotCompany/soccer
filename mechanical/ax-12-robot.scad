$fn=90;

module ax12(){
    // sort of center mass
    color("dimgray") translate([0,0,0]) import("DYNAMIXEL_AX-12A.STL");
    color("dimgray") translate([0,0,20]) import("omni-wheel.stl");
}

module base(dia){
    corner = 70;
    sx = 30;
    sy = 34;
    difference()
    {
        /* cylinder(d=dia, h=4); */
        translate([-dia/2,-dia/2,0]) cube([dia,dia,4]);
        /* translate([0,0,-1]) cylinder(d=dia/3, h=6); */
        for (i=[45, 45+90, 45+180, 45+270]){
            color("red") rotate([0,0,i]) translate([100,0,0]) translate([-corner/2,-corner/2,-1]) cube([corner,corner,6]);
            color("red") rotate([0,0,i]) translate([40,0,0]) translate([-sx/2,-sy/2,-1]) cube([2*sx,sy,6]);
        }
    }
}

base(175);


for (i=[45, 45+90, 45+180, 45+270]){
    rotate([0,0,i]) translate([-45,0,0]) rotate([0,-90,0]) ax12();
}
