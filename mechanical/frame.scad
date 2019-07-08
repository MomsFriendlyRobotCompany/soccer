

module wheel(){
    thick = 17;  // mm
    dia = 50.8;
    cylinder(h=thick, d=dia);
}

module motor(){
    cylinder(h=60, d=25);
}

module mw(angle){
    rotate([90,0,angle]){
        motor();
        translate([0,0,60]) wheel();
    }
}

translate([0,-20,0]) mw(0);
translate([20,0,0]) mw(90);
translate([0,20,0]) mw(180);
translate([-20,0,0]) mw(270);