#include "blocked.h"
#include "generate.h"
#include "segment.h"
#include "intersection.h"
#include "math.h"
#include "areas.h"
#include "heron.h"
#include <stdlib.h>
#include <stdio.h>

#ifndef M_PI
    #define M_PI 3.14159265358979323846
#endif

double blocked(double **planet, int n_layers, double x2, double y2, double r2){
    double x1,y1,r1;
    double *inner_cross,*outer_cross,*circle_cross, *first_line, *second_line;
//    double inner_cross[6] , outer_cross[6], *circle_cross, *first_line, *second_line;
    double total_blocked=0.0;
    double **crosses;

    // planet parameters

    x1 = 0;
    y1 = 0;
    r1 = 1;

    // do they intersect at all?

    double c_d = sqrt(pow(x2,2) + pow(y2,2));

    if(c_d > (r1+r2)){
        // will not intersect at all!
        return 0;
    }

    // then check for overlaps in the central circle

    double central_crossover = 0;

    if(r2 >= planet[0][14]){
        central_crossover = find_circles_region(x1,y1,planet[0][14],x2,y2,r2);
    }
    if(r2 < planet[0][14]){
        central_crossover = find_circles_region(x2-x2,y2-y2,r2,x1-x2,y1-y2,planet[0][14]);
    }

    total_blocked = total_blocked + central_crossover*planet[0][16];

    crosses = malloc(sizeof(double) * n_layers); // dynamic `array (size 4) of pointers to int`
    for (int i = 0; i < n_layers; ++i) {
      crosses[i] = malloc(sizeof(double) * 6);
      // each i-th pointer is now pointing to dynamic array of actual double values
    }


    for (int j = 0; j < n_layers; ++j) {
        double outer_r = planet[j*j][14];
        circle_cross = circle_intersect(x1,y1,outer_r,x2,y2,r2);
        for (int l = 0; l < 6; ++l) {
            crosses[j][l] = circle_cross[l];
        }
        free(circle_cross);
    }


    for (int j = 1; j < n_layers; ++j) {


        inner_cross = malloc(sizeof(double) * 6);
        outer_cross = malloc(sizeof(double) * 6);

        double inner_r = planet[j*j][13];
        double outer_r = planet[j*j][14];
        for (int l = 0; l < 6; ++l) {
            inner_cross[l] = crosses[j-1][l];
            outer_cross[l] = crosses[j][l];
        }


        for (int k = j*j; k < ((j+1)*(j+1)); ++k) {

            int n_inner = 0;
            int n_outer = 0;
            int n_first = 0;
            int n_second = 0;

            double single_inner[2];

            if((inner_cross[4] >= planet[k][10]) && (inner_cross[4] <= planet[k][11])){
                n_inner = n_inner +1;
                single_inner[0] = inner_cross[0];
                single_inner[1] = inner_cross[1];
            }

            if((inner_cross[5] >= planet[k][10]) && (inner_cross[5] <= planet[k][11])){
                n_inner = n_inner +1;
                single_inner[0] = inner_cross[2];
                single_inner[1] = inner_cross[3];
            }

            // there is a special case where circles only touch once.
            // come back and deal with this later.

            double single_outer[2];

            if((outer_cross[4] >= planet[k][10]) && (outer_cross[4] <= planet[k][11])){
                n_outer = n_outer +1;
                single_outer[0] = outer_cross[0];
                single_outer[1] = outer_cross[1];
            }

            if((outer_cross[5] >= planet[k][10]) && (outer_cross[5] <= planet[k][11])){
                n_outer = n_outer +1;
                single_outer[0] = outer_cross[2];
                single_outer[1] = outer_cross[3];
            }

            // does the first line cross?

    //        first_line = line_intersect(planet[k][4],planet[k][10],x2,y2,r2);
            first_line = line_intersect(0,0,planet[k][2],planet[k][3],x2,y2,r2);


            double single_first[2];


            // some of these logic tests are just to make sure the intersection happens on the same side//

            if((first_line[4] >= planet[k][13]) && (first_line[4] <= planet[k][14]) && ((1+first_line[0]*planet[k][2]) >= 1) && ((1 +first_line[1]*planet[k][3]) >= 1)){
                n_first = n_first +1;
                single_first[0] = first_line[0];
                single_first[1] = first_line[1];
            }

            if((first_line[5] >= planet[k][13]) && (first_line[5] <= planet[k][14]) && ((1+first_line[2]*planet[k][2]) >= 1) && ((1+first_line[3]*planet[k][3]) >= 1)){
                n_first = n_first +1;
                single_first[0] = first_line[2];
                single_first[1] = first_line[3];
            }

            // does the second line cross?
            second_line = line_intersect(0,0,planet[k][7],planet[k][8],x2,y2,r2);

            double single_second[2];

            // this test needs the +1s because of some bullshit about signed 0s


            if((second_line[4] >= planet[k][13]) && (second_line[4] <= planet[k][14]) && ((1+second_line[0]*planet[k][7]) >= 1) && ((1+second_line[1]*planet[k][8]) >= 1)){
                n_second = n_second +1;
                single_second[0] = second_line[0];
                single_second[1] = second_line[1];
            }

            if((second_line[5] >= planet[k][13]) && (second_line[5] <= planet[k][14]) && ((1+second_line[2]*planet[k][7]) >= 1) && ((1+ second_line[3]*planet[k][8]) >= 1)){
                n_second = n_second +1;
                single_second[0] = second_line[2];
                single_second[1] = second_line[3];
            }

            if((n_inner == 0) && (n_outer == 0) && (n_first == 0) && (n_second == 0)){
                double star_dist = sqrt(pow(planet[k][0] -x2,2) + pow(planet[k][1] -y2,2));
                double star_r = sqrt(pow(x2,2) + pow(y2,2));
                double theta1 = atan2(y2,x2);
                if(theta1<0){
                    theta1 = theta1 + 2*M_PI;
                }

                if(star_dist < r2){
                    total_blocked = total_blocked + planet[k][15]*planet[k][16];
                }
                else if((star_r > planet[k][13]) && (star_r <= planet[k][14]) && (theta1 > planet[k][10]) && (theta1 <= planet[k][11])){
                    total_blocked = total_blocked + (M_PI*pow(r2,2))*planet[k][16];
                }


            }
            else if((n_inner == 1) && (n_outer == 1) && (n_first == 0) && (n_second == 0)){

                // The case where the large circle crosses only the bounding circles
                // of the region

                double er1 = sqrt(pow(planet[k][0]-x2,2) + pow(planet[k][1]-y2,2));
                double er2 = sqrt(pow(planet[k][5]-x2,2) + pow(planet[k][6]-y2,2));

                double e1[2];
                double e2[2];


                if(er1 < r2){
                    e1[0] = planet[k][0];
                    e1[1] = planet[k][1];
                    e2[0] = planet[k][2];
                    e2[1] = planet[k][3];

                }
                else if(er2 < r2){
                    e1[0] = planet[k][5];
                    e1[1] = planet[k][6];
                    e2[0] = planet[k][7];
                    e2[1] = planet[k][8];

                }
                else{
                    printf("SOMETHING WRONG\n");
                    return 0;
                }

                double aa = one_in_one_out(single_inner,single_outer,e1,e2,planet[k][13],planet[k][14],r2,x2,y2);

                aa = aa*planet[k][16];

                total_blocked = total_blocked + aa;
            }

            // basically the same as the previous case, but an extra circle has to be subtracted
            else if(((n_inner == 1) && (n_outer == 1) && (n_first == 2) && (n_second == 0)) || ((n_inner == 1) && (n_outer == 1) && (n_first == 0) && (n_second == 2))){

                // The case where the large circle crosses only the bounding circles
                // of the region

                double er1 = sqrt(pow(planet[k][0]-x2,2) + pow(planet[k][1]-y2,2));
                double er2 = sqrt(pow(planet[k][5]-x2,2) + pow(planet[k][6]-y2,2));

                double e1[2];
                double e2[2];


                if(er1 < r2){
                    e1[0] = planet[k][0];
                    e1[1] = planet[k][1];
                    e2[0] = planet[k][2];
                    e2[1] = planet[k][3];

                }
                else if(er2 < r2){
                    e1[0] = planet[k][5];
                    e1[1] = planet[k][6];
                    e2[0] = planet[k][7];
                    e2[1] = planet[k][8];

                }
                else{
                    printf("SOMETHING WRONG\n");
                    return 0;
                }

                double aa1 = one_in_one_out(single_inner,single_outer,e1,e2,planet[k][13],planet[k][14],r2,x2,y2);

                double lx1[2];
                double lx2[2];

                if(n_first == 2){
                    lx1[0] = first_line[0];
                    lx1[1] = first_line[1];
                    lx2[0] = first_line[2];
                    lx2[1] = first_line[3];
                }
                else if(n_second == 2){
                    lx1[0] = second_line[0];
                    lx1[1] = second_line[1];
                    lx2[0] = second_line[2];
                    lx2[1] = second_line[3];
                }
                else{
                    printf("SOMETHING WRONG\n");
                    return 0;
                }

                double aa2 = find_segment_area(lx1,lx2,x2,y2,r2);

                double aa = (aa1-aa2)*planet[k][16];

                total_blocked = total_blocked + aa;
            }
            // the case of an outer edge and a line being crossed

            else if((n_inner == 2) && (n_outer == 0) && (n_first == 1) && (n_second == 1)){

                double er1 = sqrt(pow(planet[k][0]-x2,2) + pow(planet[k][1]-y2,2));

                double e1[2];
                double e2[2];
                double e3[2];
                double e4[2];

                double c1[2];
                double c2[2];

                double aa = 0.0;

                e1[0] = planet[k][2];
                e1[1] = planet[k][3];
                e2[0] = planet[k][7];
                e2[1] = planet[k][8];

                e3[0] = single_first[0];
                e3[1] = single_first[1];
                e4[0] = single_second[0];
                e4[1] = single_second[1];

                c1[0] = inner_cross[0];
                c1[1] = inner_cross[1];
                c2[0] = inner_cross[2];
                c2[1] = inner_cross[3];

                if(er1 > r2){
                    e1[0] = planet[k][0];
                    e1[1] = planet[k][1];
                    e2[0] = planet[k][5];
                    e2[1] = planet[k][6];
                    aa = two_inner_two_edges_a(c1,c2,e1,e2,e3,e4,planet[k][13],planet[k][14],x2,y2,r2,planet[k][15]);
                }
                else if(er1 <= r2){
                    aa = two_inner_two_edges_b(c1,c2,e1,e2,e3,e4,planet[k][13],planet[k][14],x2,y2,r2,planet[k][15]);
                }

                aa = aa*planet[k][16];

                total_blocked = total_blocked + aa;

            }

            // A nice simple case which is only a single segment
            else if(((n_inner == 0) && (n_outer == 0) && (n_first == 2) && (n_second == 0)) || ((n_inner == 0) && (n_outer == 0) && (n_first == 0) && (n_second == 2))){

                double lx1[2];
                double lx2[2];

                if(n_first == 2){
                    lx1[0] = first_line[0];
                    lx1[1] = first_line[1];
                    lx2[0] = first_line[2];
                    lx2[1] = first_line[3];
                }
                else if(n_second == 2){
                    lx1[0] = second_line[0];
                    lx1[1] = second_line[1];
                    lx2[0] = second_line[2];
                    lx2[1] = second_line[3];
                }
                else{
                    printf("SOMETHING WRONG\n");
                    return 0;
                }

                double aa = find_segment_area(lx1,lx2,x2,y2,r2);

                aa = aa*planet[k][16];

                total_blocked = total_blocked + aa;
            }
            // the case of an outer edge and a line being crossed
            // ACTUALLY THIS IS TWO CASES!
            else if( ( (n_inner == 0) && (n_outer == 1) && (n_first == 1) && (n_second == 0) ) || ( (n_inner == 0) && (n_outer == 1) && (n_first == 0) && (n_second == 1) ) ){

                double er1 = sqrt(pow(planet[k][0]-x2,2) + pow(planet[k][1]-y2,2));
                double er2 = sqrt(pow(planet[k][5]-x2,2) + pow(planet[k][6]-y2,2));
                double er3 = sqrt(pow(planet[k][2]-x2,2) + pow(planet[k][3]-y2,2));
                double er4 = sqrt(pow(planet[k][7]-x2,2) + pow(planet[k][8]-y2,2));

                double e1[2];
                double e2[2];

                int corners_inside = 0;

                if(er1 < r2){
                    corners_inside = corners_inside +1;
                }
                if(er2 < r2){
                    corners_inside = corners_inside +1;
                }
                if(er3 < r2){
                    corners_inside = corners_inside +1;
                }
                if(er4 < r2){
                    corners_inside = corners_inside +1;
                }

                // which of the corner points is inside?

                if(n_first == 1){
                    e1[0] = single_first[0];
                    e1[1] = single_first[1];
                }
                else{
                    e1[0] = single_second[0];
                    e1[1] = single_second[1];
                }

                if(corners_inside == 3){
                    if(er1 > r2){
                        e2[0] = planet[k][0];
                        e2[1] = planet[k][1];

                    }
                    else if(er2 > r2){
                        e2[0] = planet[k][5];
                        e2[1] = planet[k][6];
                    }
                    else if(er3 > r2){
                        e2[0] = planet[k][2];
                        e2[1] = planet[k][3];
                    }
                    else if(er4 > r2){
                        e2[0] = planet[k][7];
                        e2[1] = planet[k][8];
                    }
                    else{
                        printf("SOMETHING WRONG\n");
                        return 0;
                    }
                }
                else if(corners_inside == 1){
                    if(er1 < r2){
                        e2[0] = planet[k][0];
                        e2[1] = planet[k][1];

                    }
                    else if(er2 < r2){
                        e2[0] = planet[k][5];
                        e2[1] = planet[k][6];
                    }
                    else if(er3 < r2){
                        e2[0] = planet[k][2];
                        e2[1] = planet[k][3];
                    }
                    else if(er4 < r2){
                        e2[0] = planet[k][7];
                        e2[1] = planet[k][8];
                    }
                    else{
                        printf("SOMETHING WRONG\n");
                        return 0;
                    }
                }
                else{
                        printf("SOMETHING WRONG\n");
                        return 0;
                }

                double aa = 0;

                if(corners_inside == 3){
                    aa = one_edge_one_outer_b(single_outer,e1,e2,planet[k][13],planet[k][14],r2,x2,y2,planet[k][15]);
                }
                else if(corners_inside == 1){
                    aa = one_edge_one_outer_a(single_outer,e1,e2,planet[k][13],planet[k][14],r2,x2,y2);
                }
                else{
                }

                aa = aa*planet[k][16];

                total_blocked = total_blocked + aa;
            }

            // the case where an inner edge, and either of the sides is crossed 
            else if( ( (n_inner == 1) && (n_outer == 0) && (n_first == 1) && (n_second == 0) ) || ( (n_inner == 1) && (n_outer == 0) && (n_first == 0) && (n_second == 1) ) ){

                double er1 = sqrt(pow(planet[k][0]-x2,2) + pow(planet[k][1]-y2,2));
                double er2 = sqrt(pow(planet[k][5]-x2,2) + pow(planet[k][6]-y2,2));
                double er3 = sqrt(pow(planet[k][2]-x2,2) + pow(planet[k][3]-y2,2));
                double er4 = sqrt(pow(planet[k][7]-x2,2) + pow(planet[k][8]-y2,2));

                double e1[2];
                double e2[2];

                int corners_inside = 0;

                if(er1 < r2){
                    corners_inside = corners_inside +1;
                }
                if(er2 < r2){
                    corners_inside = corners_inside +1;
                }
                if(er3 < r2){
                    corners_inside = corners_inside +1;
                }
                if(er4 < r2){
                    corners_inside = corners_inside +1;
                }

                // which of the corner points is inside?
                if(n_first == 1){
                    e1[0] = single_first[0];
                    e1[1] = single_first[1];
                }
                else{
                    e1[0] = single_second[0];
                    e1[1] = single_second[1];
                }


                // instead of this mess, just use a sort algorithm.
                if(corners_inside == 3){
                    if(er1 > r2){
                        e2[0] = planet[k][0];
                        e2[1] = planet[k][1];

                    }
                    else if(er2 > r2){
                        e2[0] = planet[k][5];
                        e2[1] = planet[k][6];
                    }
                    else if(er3 > r2){
                        e2[0] = planet[k][2];
                        e2[1] = planet[k][3];
                    }
                    else if(er4 > r2){
                        e2[0] = planet[k][7];
                        e2[1] = planet[k][8];
                    }
                    else{
                        printf("SOMETHING WRONG\n");
                        return 0;
                    }
                }
                else if(corners_inside == 1){
                    if(er1 < r2){
                        e2[0] = planet[k][0];
                        e2[1] = planet[k][1];

                    }
                    else if(er2 < r2){
                        e2[0] = planet[k][5];
                        e2[1] = planet[k][6];
                    }
                    else if(er3 < r2){
                        e2[0] = planet[k][2];
                        e2[1] = planet[k][3];
                    }
                    else if(er4 < r2){
                        e2[0] = planet[k][7];
                        e2[1] = planet[k][8];
                    }
                    else{
                        printf("SOMETHING WRONG\n");
                        return 0;
                    }
                }
                else{
                        printf("SOMETHING WRONG\n");
                        return 0;
                }

                // this has to be split into two cases!!!

                double aa = 0;
                if(corners_inside == 3){
                    aa = one_edge_one_inner_b(single_inner,e1,e2,planet[k][13],planet[k][14],r2,x2,y2,planet[k][15]);
                }
                else if(corners_inside == 1){
                    double *new_line = line_intersect(single_inner[0],single_inner[1],e1[0],e1[1],0,0,planet[k][13]);
                    aa = one_edge_one_inner_a(single_inner,e1,e2,planet[k][13],planet[k][14],r2,x2,y2);

                    double c1[2];
                    double c2[2];

                    c1[0] = new_line[0];
                    c1[1] = new_line[1];

                    c2[0] = new_line[2];
                    c2[1] = new_line[3];

                    double new = find_segment_area(c1,c2,0,0,planet[k][13]);

                    free(new_line);

                }
                else{
                    printf("CASE NOT RECOGNISED\n");
                }


                aa = aa*planet[k][16];

                total_blocked = total_blocked + aa;

            }
            // this one is simple - just circles crossing, edges not involved
            // slightly worse if the circle is coming from the inside
            else if((n_inner == 0) && (n_outer == 2) && (n_first == 0) && (n_second == 0)){

                double circle_crossover = 0.0;

                double er1 = sqrt(pow(planet[k][0]-x2,2) + pow(planet[k][1]-y2,2));

                double c1[2];
                double c2[2];

                c1[0]=outer_cross[0];
                c1[1]=outer_cross[1];
                c2[0]=outer_cross[2];
                c2[1]=outer_cross[3];

                if(er1>r2){
                    if(r2 >= planet[k][14]){
                        circle_crossover = find_circles_region(x1,y1,planet[k][14],x2,y2,r2);
                    }
                    if(r2 < planet[k][14]){
                        circle_crossover = find_circles_region(x2-x2,y2-y2,r2,x1-x2,y1-y2,planet[k][14]);
                    }
                    total_blocked = total_blocked + circle_crossover*planet[k][16];
                }

                else{
                    double a_1 = find_segment_area(c1,c2,0,0,planet[k][14]);
                    double a_2 = find_segment_area(c1,c2,x2,y2,r2);
                    double area = planet[k][15] - (a_1 - a_2);
                    total_blocked = total_blocked + area*planet[k][16];
                }

            }

            // in this one two edges are crossed, and nothing else (note, this one should have two versions)
            // depending on whether the outer or inner edges are inside
            else if((n_inner == 0) && (n_outer == 0) && (n_first == 1) && (n_second == 1)){

                double er1 = sqrt(pow(planet[k][0]-x2,2) + pow(planet[k][1]-y2,2));

                double e1[2];
                double e2[2];
                double e3[2];
                double e4[2];

                double aa = 0.0;

                if(er1 < r2){
                    // in this case the *inner* edges are inside
                    e1[0] = single_first[0];
                    e1[1] = single_first[1];

                    e2[0] = single_second[0];
                    e2[1] = single_second[1];

                    e3[0] = planet[k][0];
                    e3[1] = planet[k][1];

                    e4[0] = planet[k][5];
                    e4[1] = planet[k][6];

                    aa = two_edges_a(e1,e2,e3,e4,planet[k][13],x2,y2,r2,planet[k][12],planet[k][10],planet[k][11]);
                }
                else{
                    // in this case the *outer* edges are inside
                    e1[0] = single_first[0];
                    e1[1] = single_first[1];

                    e2[0] = single_second[0];
                    e2[1] = single_second[1];

                    e3[0] = planet[k][2];
                    e3[1] = planet[k][3];

                    e4[0] = planet[k][7];
                    e4[1] = planet[k][8];

                    aa = two_edges_b(e1,e2,e3,e4,planet[k][14],x2,y2,r2);
                }


                aa = aa*planet[k][16];

                total_blocked = total_blocked + aa;
            }
            else if(((n_inner == 2) && (n_outer == 1) && (n_first == 1) && (n_second == 0)) || ((n_inner == 2) && (n_outer == 1) && (n_first == 0) && (n_second == 1))){

                // This case is similar to the triangle case, but has to have an additional circle crossover removed.

                double er1 = sqrt(pow(planet[k][0]-x2,2) + pow(planet[k][1]-y2,2));
                double er2 = sqrt(pow(planet[k][5]-x2,2) + pow(planet[k][6]-y2,2));
                double er3 = sqrt(pow(planet[k][2]-x2,2) + pow(planet[k][3]-y2,2));
                double er4 = sqrt(pow(planet[k][7]-x2,2) + pow(planet[k][8]-y2,2));

                double e1[2];
                double e2[2];


                // which of the corner points is inside?
                if(n_first == 1){
                    e1[0] = single_first[0];
                    e1[1] = single_first[1];
                }
                else{
                    e1[0] = single_second[0];
                    e1[1] = single_second[1];
                }


                // instead of this mess, just use a sort algorithm.
                // it's safer, too
                if(er1 < r2){
                    e2[0] = planet[k][0];
                    e2[1] = planet[k][1];
                }
                else if(er2 < r2){
                    e2[0] = planet[k][5];
                    e2[1] = planet[k][6];
                }
                else if(er3 < r2){
                    e2[0] = planet[k][2];
                    e2[1] = planet[k][3];
                }
                else if(er4 < r2){
                    e2[0] = planet[k][7];
                    e2[1] = planet[k][8];
                }
                else{
                    printf("SOMETHING WRONG\n");
                    return 0;
                }

                double aa = 0.0;
                if(er1 > r2){
                    aa = one_edge_two_inner_one_outer_a(single_outer,e1,e2,planet[k][13],planet[k][14],r2,x2,y2);
                }
                else{

                    double c1[2];
                    double c2[2];
                    double e3[2];
                    double e4[2];


                    e3[0] = planet[k][0];
                    e3[1] = planet[k][1];

                    e4[0] = planet[k][5];
                    e4[1] = planet[k][6];

                    c1[0] = inner_cross[0];
                    c1[1] = inner_cross[1];
                    c2[0] = inner_cross[2];
                    c2[1] = inner_cross[3];

                    double er1 = sqrt(pow(planet[k][2]-single_outer[0],2) + pow(planet[k][3]-single_outer[1],2));
                    double er2 = sqrt(pow(planet[k][7]-single_outer[0],2) + pow(planet[k][8]-single_outer[1],2));

                    if(er1 < er2){
                        e2[0] = planet[k][2];
                        e2[1] = planet[k][3];
                    }
                    else{
                        e2[0] = planet[k][7];
                        e2[1] = planet[k][8];
                    }

                    aa = one_edge_two_inner_one_outer_b(single_outer,e1,e2,e3,e4,c1,c2,planet[k][13],planet[k][14],r2,x2,y2);

                }

                aa = aa*planet[k][16];

                total_blocked = total_blocked + aa;
            }
//            else if(((n_inner == 0) && (n_outer == 2) && (n_first == 1) && (n_second == 0)) || ((n_inner == 0) && (n_outer == 2) && (n_first == 0) && (n_second == 1))){
    //          this is a tangent solution, ignore it
//            }

//            else if(((n_inner == 0) && (n_outer == 0) && (n_first == 0) && (n_second == 1)) || ((n_inner == 0) && (n_outer == 0) && (n_first == 1) && (n_second == 0))){
    //          this is a tangent solution, ignore it
//            }

            else if((n_inner == 0) && (n_outer == 2) && (n_first == 1) && (n_second == 1)){

                double e1[2];
                double e2[2];
                double e3[2];
                double e4[2];
                double e5[2];
                double e6[2];

                double c1[2];
                double c2[2];
                double c3[2];
                double c4[2];

                c1[0]=outer_cross[0];
                c1[1]=outer_cross[1];
                c2[0]=outer_cross[2];
                c2[1]=outer_cross[3];

                double aa = 0.0;


                e1[0] = single_first[0];
                e1[1] = single_first[1];

                e2[0] = single_second[0];
                e2[1] = single_second[1];

                e3[0] = planet[k][0];
                e3[1] = planet[k][1];

                e4[0] = planet[k][5];
                e4[1] = planet[k][6];

                aa = two_edges_a(e1,e2,e3,e4,planet[k][13],x2,y2,r2,planet[k][12],planet[k][10],planet[k][11]);

                double circle_crossover = 0.0;

                if(r2 >= planet[k][14]){
                    circle_crossover = find_circles_region(x1,y1,planet[k][14],x2,y2,r2);
                }
                if(r2 < planet[k][14]){
                    circle_crossover = find_circles_region(x2-x2,y2-y2,r2,x1-x2,y1-y2,planet[k][14]);
                }

/*                debug 
                double adjust = (M_PI*pow(r2,2) - circle_crossover);
                printf("ADJUST %f\n",adjust);
                aa = aa - adjust;
*/

                // in this case the *inner* edges are inside
/*                e1[0] = single_first[0];
                e1[1] = single_first[1];

                e2[0] = single_second[0];
                e2[1] = single_second[1];

                e3[0] = planet[k][0];
                e3[1] = planet[k][1];

                e4[0] = planet[k][5];
                e4[1] = planet[k][6];

                e5[0] = planet[k][2];
                e5[1] = planet[k][3];

                e6[0] = planet[k][7];
                e6[1] = planet[k][8];

                double er1 = sqrt(pow(e1[0]-c1[0],2) + pow(e1[1]-c1[1],2));
                double er2 = sqrt(pow(e1[0]-c2[0],2) + pow(e1[1]-c2[1],2));

                if(er1 <= er2){
                    aa = find_triangle_area(e1,c1,e6) + find_segment_area(c1,e6,0,0,planet[k][13])- find_segment_area(c1,e1,x2,y2,r2);
                    aa = aa + find_triangle_area(e2,c2,e6) + find_segment_area(c2,e4,0,0,planet[k][13])- find_segment_area(c2,e2,x2,y2,r2);
                }

                if(er1 > er2){
                    aa = find_triangle_area(e1,c2,e6) + find_segment_area(c2,e6,0,0,planet[k][13])- find_segment_area(c2,e1,x2,y2,r2);
                    aa = aa + find_triangle_area(e2,c1,e6) + find_segment_area(c1,e4,0,0,planet[k][13])- find_segment_area(c1,e2,x2,y2,r2);
                }

                aa = planet[k][15] - aa; */



                aa = aa*planet[k][16];

                total_blocked = total_blocked + aa;
            }

            else if((n_inner == 2) && (n_outer == 2) && (n_first == 0) && (n_second == 0)){
    //          Almost forgot about this one...

                double c1[2];
                double c2[2];
                double c3[2];
                double c4[2];

                c1[0]=outer_cross[0];
                c1[1]=outer_cross[1];
                c2[0]=outer_cross[2];
                c2[1]=outer_cross[3];

                c3[0]=inner_cross[0];
                c3[1]=inner_cross[1];
                c4[0]=inner_cross[2];
                c4[1]=inner_cross[3];

//                double a_1 = find_segment_area(c1,c2,x2,y2,r2);
//                double a_2 = find_segment_area(c1,c2,0,0,planet[k][14]);

//                double a_3 = find_segment_area(c3,c4,x2,y2,r2);
//                double a_4 = find_segment_area(c3,c4,0,0,planet[k][13]);
//                double aa = a_1 + a_2 - (a_3 + a_4);

                double a_1 = find_quad_area(c1,c2,c3,c4);
                double a_4 = find_segment_area(c1,c2,0,0,planet[k][14]);
                double a_5 = find_segment_area(c3,c4,0,0,planet[k][13]);

                double er1 = sqrt(pow(c1[0]-c3[0],2) + pow(c1[1]-c3[1],2));
                double er2 = sqrt(pow(c1[0]-c4[0],2) + pow(c1[1]-c4[1],2));

                double a_2 = find_segment_area(c1,c3,x2,y2,r2);
                double a_3 = find_segment_area(c2,c4,x2,y2,r2);

                if(er2 < er1){
                    a_2 = find_segment_area(c1,c4,x2,y2,r2);
                    a_3 = find_segment_area(c2,c3,x2,y2,r2);
                }


                double aa = a_1 + a_2 + a_3 + a_4 - a_5;
                aa = aa*planet[k][16];

                total_blocked = total_blocked + aa;


            }

            else if((n_inner == 2) && (n_outer == 0) && (n_first == 0) && (n_second == 0)){


                double circle_crossover = 0.0;

                if(r2 >= planet[k][13]){
                    circle_crossover = find_circles_region(x1,y1,planet[k][13],x2,y2,r2);
                }
                if(r2 < planet[k][13]){
                    circle_crossover = find_circles_region(x2-x2,y2-y2,r2,x1-x2,y1-y2,planet[k][13]);
                }

                double overlap = (M_PI*pow(r2,2) - circle_crossover);

                total_blocked = total_blocked + overlap*planet[k][16];


            }

            else if((n_inner == 2) && (n_outer == 2) && (n_first == 2) && (n_second == 2)){

                double e1[2];
                double e2[2];
                double e3[2];
                double e4[2];

                double oc1[2];
                double oc2[2];
                double ic1[2];
                double ic2[2];
                double fc1[2];
                double fc2[2];
                double sc1[2];
                double sc2[2];

                if(outer_cross[4] < outer_cross[5]){
                    oc1[0]=outer_cross[0];
                    oc1[1]=outer_cross[1];
                    oc2[0]=outer_cross[2];
                    oc2[1]=outer_cross[3];
                }
                else{
                    oc1[0]=outer_cross[2];
                    oc1[1]=outer_cross[3];
                    oc2[0]=outer_cross[0];
                    oc2[1]=outer_cross[1];
                }

                if(inner_cross[4] < inner_cross[5]){
                    ic1[0]=inner_cross[0];
                    ic1[1]=inner_cross[1];
                    ic2[0]=inner_cross[2];
                    ic2[1]=inner_cross[3];
                }
                else{
                    ic1[0]=inner_cross[2];
                    ic1[1]=inner_cross[3];
                    ic2[0]=inner_cross[0];
                    ic2[1]=inner_cross[1];
                }

                if(first_line[4] < first_line[5]){
                    fc1[0]=first_line[0];
                    fc1[1]=first_line[1];
                    fc2[0]=first_line[2];
                    fc2[1]=first_line[3];
                }
                else{
                    fc1[0]=first_line[2];
                    fc1[1]=first_line[3];
                    fc2[0]=first_line[0];
                    fc2[1]=first_line[1];
                }


                if(second_line[4] < second_line[5]){
                    sc1[0]=second_line[0];
                    sc1[1]=second_line[1];
                    sc2[0]=second_line[2];
                    sc2[1]=second_line[3];
                }
                else{
                    sc1[0]=second_line[2];
                    sc1[1]=second_line[3];
                    sc2[0]=second_line[0];
                    sc2[1]=second_line[1];
                }

                e1[0] = planet[k][0];
                e1[1] = planet[k][1];
                e2[0] = planet[k][2];
                e2[1] = planet[k][3];
                e3[0] = planet[k][5];
                e3[1] = planet[k][6];
                e4[0] = planet[k][7];
                e4[1] = planet[k][8];


                double a_1 = find_triangle_area(e1,fc1,ic1) - find_segment_area(fc1,ic1,0,0,planet[k][13]) - find_segment_area(e1,ic1,x2,y2,r2);

                double a_2 = find_triangle_area(e2,fc2,oc1) + find_segment_area(fc2,oc1,0,0,planet[k][14]) - find_segment_area(e2,oc1,x2,y2,r2);

                double a_3 = find_triangle_area(e3,sc1,ic2) - find_segment_area(sc1,ic2,0,0,planet[k][13]) - find_segment_area(e3,ic2,x2,y2,r2);


                double a_4 = find_triangle_area(e4,sc2,oc2) + find_segment_area(sc2,oc2,0,0,planet[k][14]) - find_segment_area(e4,oc2,x2,y2,r2);

                double area = planet[k][15] - (a_1 + a_2 + a_3 + a_4);

                total_blocked = total_blocked + area*planet[k][16];


            }

            else if(((n_inner == 2) && (n_outer == 2) && (n_first == 0) && (n_second == 2)) || ((n_inner == 2) && (n_outer == 2) && (n_first == 2) && (n_second == 0))){

                double e1[2];
                double e2[2];
                double e3[2];
                double e4[2];

                double oc1[2];
                double oc2[2];
                double ic1[2];
                double ic2[2];
                double fc1[2];
                double fc2[2];
                double sc1[2];
                double sc2[2];

                double lx1[2];
                double lx2[2];

                if(n_first == 2){
                	if(first_line[4] < first_line[5]){
	                    lx1[0] = first_line[0];
	                    lx1[1] = first_line[1];
	                    lx2[0] = first_line[2];
	                    lx2[1] = first_line[3];
	                }
	                else{
	                    lx2[0] = first_line[0];
	                    lx2[1] = first_line[1];
	                    lx1[0] = first_line[2];
	                    lx1[1] = first_line[3];
	                   }
                }
                else if(n_second == 2){
                	if(second_line[4] < second_line[5]){
	                    lx1[0] = second_line[0];
	                    lx1[1] = second_line[1];
	                    lx2[0] = second_line[2];
	                    lx2[1] = second_line[3];
	                }
	                else{
	                    lx2[0] = second_line[0];
	                    lx2[1] = second_line[1];
	                    lx1[0] = second_line[2];
	                    lx1[1] = second_line[3];
	                   }
                }
                else{
                    printf("SOMETHING WRONG\n");
                    return 0;
                }

                double er1 = sqrt(pow(outer_cross[0]-lx2[0],2) + pow(outer_cross[1]-lx2[1],2));
                double er2 = sqrt(pow(outer_cross[2]-lx2[0],2) + pow(outer_cross[3]-lx2[1],2));

                if(er1 < er2){
                    oc1[0]=outer_cross[0];
                    oc1[1]=outer_cross[1];
                    oc2[0]=outer_cross[2];
                    oc2[1]=outer_cross[3];
                }
                else{
                    oc1[0]=outer_cross[2];
                    oc1[1]=outer_cross[3];
                    oc2[0]=outer_cross[0];
                    oc2[1]=outer_cross[1];
                }

                er1 = sqrt(pow(inner_cross[0]-lx1[0],2) + pow(inner_cross[1]-lx1[1],2));
                er2 = sqrt(pow(inner_cross[2]-lx1[0],2) + pow(inner_cross[3]-lx1[1],2));

                if(er1 < er2){
                    ic1[0]=inner_cross[0];
                    ic1[1]=inner_cross[1];
                    ic2[0]=inner_cross[2];
                    ic2[1]=inner_cross[3];
                }
                else{
                    ic1[0]=inner_cross[2];
                    ic1[1]=inner_cross[3];
                    ic2[0]=inner_cross[0];
                    ic2[1]=inner_cross[1];
                }

                double a_1 = find_quad_area(ic1,ic2,oc1,oc2);

                double a_2 = find_segment_area(oc1,oc2,0.0,0.0,planet[k][14]);
                double a_3 = find_segment_area(ic1,ic2,0.0,0.0,planet[k][13]);


                double a_4 = find_segment_area(ic2,oc2,x2,y2,r2);
                double a_5 = find_segment_area(ic1,oc1,x2,y2,r2);
                double a_6 = find_segment_area(lx1,lx2,x2,y2,r2);

                double area = (a_1 + a_2 - a_3 + a_4  + a_5 - a_6);

                total_blocked = total_blocked + area*planet[k][16];


            }

            else if(((n_inner == 1) && (n_outer == 2) && (n_first == 1) && (n_second == 0)) || ((n_inner == 1) && (n_outer == 2) && (n_first == 0) && (n_second == 1))){

                // A case only relevent to small star cases.

                double e1[2];
                double e2[2];
                double c1[2];
                double c2[2];


                if(n_first == 1){
                    e1[0] = single_first[0];
                    e1[1] = single_first[1];
                }
                else{
                    e1[0] = single_second[0];
                    e1[1] = single_second[1];
                }


                // which of the corner points is inside?
                double er1 = sqrt(pow(planet[k][0]-x2,2) + pow(planet[k][1]-y2,2));
                double er2 = sqrt(pow(planet[k][5]-x2,2) + pow(planet[k][6]-y2,2));
                double er3 = sqrt(pow(planet[k][2]-x2,2) + pow(planet[k][3]-y2,2));
                double er4 = sqrt(pow(planet[k][7]-x2,2) + pow(planet[k][8]-y2,2));
                if(er1 < r2){
                    e2[0] = planet[k][0];
                    e2[1] = planet[k][1];
                }
                else if(er2 < r2){
                    e2[0] = planet[k][5];
                    e2[1] = planet[k][6];
                }
                else if(er3 < r2){
                    e2[0] = planet[k][2];
                    e2[1] = planet[k][3];
                }
                else if(er4 < r2){
                    e2[0] = planet[k][7];
                    e2[1] = planet[k][8];
                }
                else{
                    printf("SOMETHING WRONG\n");
                    return 0;
                }

                // sort the outer cross points so that c1 is the one closest to the covered corner

                double cd1 = sqrt(pow(outer_cross[0]-e2[0],2) + pow(outer_cross[1]-e2[1],2));
                double cd2 = sqrt(pow(outer_cross[2]-e2[0],2) + pow(outer_cross[3]-e2[1],2));
                if(cd1 < cd2){
	                c1[0]=outer_cross[0];
	                c1[1]=outer_cross[1];
	                c2[0]=outer_cross[2];
	                c2[1]=outer_cross[3];
                }
                else{
	                c2[0]=outer_cross[0];
	                c2[1]=outer_cross[1];
	                c1[0]=outer_cross[2];
	                c1[1]=outer_cross[3];
                }

                double aa = 0.0;
                aa = one_edge_two_outer_one_inner(c1,c2,single_inner,e1,e2,planet[k][13],planet[k][14],r2,x2,y2);

                aa = aa*planet[k][16];

                total_blocked = total_blocked + aa;
            }


            else{
                printf("UNKNOWN CASE: n_first %i n_second %i n_inner %i n_outer %i star x %f star y %f star r %f \n", n_first, n_second, n_inner, n_outer, x2, y2, r2);
                return 0;
            }

//			  DEBUG
//            double simple_fit = find_circles_region(x1,y1,planet[k][14],x2,y2,r2)/M_PI;

    //        printf("total_blocked %f\n",total_blocked);
    //        printf("simple fit: %f\n",simple_fit);
    //        printf("dif: %f\n",total_blocked-simple_fit);
            free(first_line);
            free(second_line);

        }
        free(inner_cross);
        free(outer_cross);

    }

    for (int j = 0; j < n_layers; ++j) {
        free(crosses[j]);
    }
    free(crosses);

//    DEBUG
//    double simple_fit = find_circles_region(x1,y1,r1,x2,y2,r2)/M_PI;
//    printf("simple fit: %f\n",simple_fit);

//    printf("total_blocked: %f (%f different to circle/cirlce)\n",total_blocked,total_blocked-simple_fit);

    return total_blocked;
}
