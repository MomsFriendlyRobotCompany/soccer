$fn=90;

// DC motor
module motor(){
    rotate([0,90,0]) {
        color("silver") translate([0,0,-16]) cylinder(h=12,d=4);  // shaft
        color("gray") translate([0,0,-4]) cylinder(h=4, d=9);     // nubbin
        difference(){
            color("gray") cylinder(h=20, d=25);                   // gears
            translate([21/2,0,-1]) cylinder(h=5, d=3);            // mounting hole
            translate([-21/2,0,-1]) cylinder(h=5, d=3);           // mounting hole
        }
        color("silver") translate([0,0,20]) cylinder(h=22, d=23); // motor
        color("gray") translate([0,0,42]) cylinder(h=3, d=10);    // motor nubbin
    }
}

// metal hub between wheel and motor
module hub(){
    color("silver") rotate([0,90,0]) {
        cylinder(h=3, d=9);
        translate([0,0,3]) cylinder(h=6, d=22);
        translate([0,0,9]) cylinder(h=3, d=9);
    }
}

// omni wheel
module wheel(){
    rotate([0,90,0]) color("lightblue") difference(){
        cylinder(h=17, d=49, center=true);
        cylinder(h=20, d=7, center=true);
    }
        
    for(a = [0:7]){
        rotate([a*45,0,0]) translate([0,22,0]) color("white") cylinder(h=12,d=9, center=true);
    }
}

// combined motor, hub, and wheel assembly
module wheel_seg(){
    motor();
    translate([-16,0,0]) hub();
    translate([-16-17/2,0,0]) wheel();
}

// mounting frame for motor
module motor_mnt(){
    difference(){
        cube([2,30,30]);
    }
}

module ir_mnt(){
    translate([-3/2,-25/2,0]) cube([3,25,10]);
}

module motor_plate(dia, draw=false){
    if (draw){
        translate([0,0,25/2+4]){
            mdis = [-dia/4-5,0,0];
            translate(mdis) wheel_seg();
            rotate([0,0,90]) translate(mdis) wheel_seg();
            rotate([0,0,180]) translate(mdis) wheel_seg();
            rotate([0,0,270]) translate(mdis) wheel_seg();
        }
    }

    difference(){
        cylinder(h=3, d=dia);
        translate([80,0,0]) cube([20,55,20], center=true);
        rotate([0,0,90]) translate([80,0,0]) cube([20,55,20], center=true);
        rotate([0,0,180]) translate([80,0,0]) cube([20,55,20], center=true);
        rotate([0,0,270]) translate([80,0,0]) cube([20,55,20], center=true);
    }
    
    for(a=[0:3]){
        rotate([0,0,90*a]) translate([-57.5,-15,0]) motor_mnt();
        rotate([0,0,90*a+45]) translate([0.8*dia/2,0,3]) ir_mnt();
    }
}

motor_plate(200, true);

