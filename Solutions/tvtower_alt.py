


class TVTower(object):
    def minRadius(self, x, y):
        eps = 1e-12
        # N = x.size();
        N = len(x)

        # mnX = *min_element(x.begin(), x.end());
        # mxX = *max_element(x.begin(), x.end());
        # mnY = *min_element(y.begin(), y.end());
        # mxY = *max_element(y.begin(), y.end());
        # double ret = 0.0;
        minRad = 0.0
        # double	l = mnX, r = mxX;
        l = min(x)
        r = max(x)
        # while(l <= r && abs(r-l) > eps) {
        while (l<=r and abs(r-l)>eps):
        # 	double ml = l + (r-l)/3;
        ml = l + (r-l)/3
        # 	double ly = findY(ml);
        ly = #!!!!
        # 	double dist_l = getDistance(ml, ly);
        #
        # 	double mr = l + 2*(r-l)/3;
        # 	double ry = findY(mr);
        # 	double dist_r = getDistance(mr, ry);
        #
        #
        # 	if(abs(dist_l - dist_r) < eps) {
        # 		l = ml;
        # 		r = mr;
        # 	}
        # 	else if(dist_l < dist_r)
        # 		r = mr;
        # 	else
        # 		l = ml;
        # }
        # double xx = l;
        # double yy = findY(xx);
        # double dist = getDistance(xx, yy);
        # ret = sqrt(dist);
        #
        # return ret;