#include <cassert>
#include "../firmware/room-climate-hub-mobile-alerts/alert_policy.h"
int main(){AlertPolicy p;assert(p.update(29,50,1013)&&!p.active);p.update(30,50,1013);p.update(30,50,1013);assert(!p.active);p.update(30,50,1013);assert(p.active);p.update(29,50,1013);assert(p.active);p.update(28,50,1013);assert(!p.active);p.update(31,50,1013);assert(!p.update(NAN,50,1013)&&!p.active&&p.confirmations==0);assert(!p.update(20,101,1013));assert(!p.update(20,50,299));p.update(30,50,1013);p.update(29,50,1013);p.update(30,50,1013);assert(p.confirmations==1);}
