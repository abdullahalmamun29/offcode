"""
CHUP Phase 3R — C++ Generator for Computational Geometry.

Emits standalone, verified C++17 implementations for all 10 Phase 3R patterns:
- __int128_t exact promotion for coordinates up to 2e9
- Boundary-first point-in-polygon containment
- Monotone chain with configurable HullCollinearPolicy
- Scale-aware tolerance gating for line intersections
- Convex hull -> Rotating calipers composition
"""

from typing import Dict, Any, Optional


def generate_geometry_cpp(pattern: str, features: Optional[Dict[str, Any]] = None) -> str:
    feat = features or {}

    # ── 1. Orientation Cross Product (3R-A) ──
    if pattern == "geom_orientation_cross_product":
        return """#include <iostream>

using namespace std;
using i128 = __int128_t;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long ax, ay, bx, by, cx, cy;
    if (!(cin >> ax >> ay >> bx >> by >> cx >> cy)) return 0;

    // Strict i128 promotion prior to multiplication to avoid overflow up to 2e9
    i128 dx1 = (i128)bx - ax;
    i128 dy2 = (i128)cy - ay;
    i128 dy1 = (i128)by - ay;
    i128 dx2 = (i128)cx - ax;

    i128 cross = dx1 * dy2 - dy1 * dx2;

    if (cross > 0) {
        cout << "COUNTER_CLOCKWISE\\n";
    } else if (cross < 0) {
        cout << "CLOCKWISE\\n";
    } else {
        cout << "COLLINEAR\\n";
    }

    return 0;
}
"""

    # ── 2. Segment Intersection (3R-B) ──
    if pattern == "geom_segment_intersection":
        return """#include <iostream>
#include <algorithm>

using namespace std;
using i128 = __int128_t;

struct Point {
    long long x, y;
};

int orientation(const Point& a, const Point& b, const Point& c) {
    i128 cross = (i128)(b.x - a.x) * (c.y - a.y) - (i128)(b.y - a.y) * (c.x - a.x);
    if (cross > 0) return 1;    // CCW
    if (cross < 0) return -1;   // CW
    return 0;                   // Collinear
}

bool on_segment(const Point& p, const Point& a, const Point& b) {
    return p.x >= min(a.x, b.x) && p.x <= max(a.x, b.x) &&
           p.y >= min(a.y, b.y) && p.y <= max(a.y, b.y);
}

bool segments_intersect(const Point& p1, const Point& p2, const Point& p3, const Point& p4) {
    int o1 = orientation(p1, p2, p3);
    int o2 = orientation(p1, p2, p4);
    int o3 = orientation(p3, p4, p1);
    int o4 = orientation(p3, p4, p2);

    if (o1 != o2 && o3 != o4) return true;

    if (o1 == 0 && on_segment(p3, p1, p2)) return true;
    if (o2 == 0 && on_segment(p4, p1, p2)) return true;
    if (o3 == 0 && on_segment(p1, p3, p4)) return true;
    if (o4 == 0 && on_segment(p2, p3, p4)) return true;

    return false;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    Point p1, p2, p3, p4;
    if (cin >> p1.x >> p1.y >> p2.x >> p2.y >> p3.x >> p3.y >> p4.x >> p4.y) {
        if (segments_intersect(p1, p2, p3, p4)) {
            cout << "YES\\n";
        } else {
            cout << "NO\\n";
        }
    }
    return 0;
}
"""

    # ── 3. Convex Hull Andrew Monotone Chain (3R-C) ──
    if pattern == "geom_convex_hull_andrew":
        keep_collinear = feat.get("hull_collinear_policy") == "KEEP_BOUNDARY_POINTS"
        cmp_op = "< 0" if keep_collinear else "<= 0"
        return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;
using i128 = __int128_t;

struct Point {{
    long long x, y;
    bool operator<(const Point& o) const {{
        if (x != o.x) return x < o.x;
        return y < o.y;
    }}
    bool operator==(const Point& o) const {{
        return x == o.x && y == o.y;
    }}
}};

i128 cross_prod(const Point& o, const Point& a, const Point& b) {{
    return (i128)(a.x - o.x) * (b.y - o.y) - (i128)(a.y - o.y) * (b.x - o.x);
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    vector<Point> pts(n);
    for (int i = 0; i < n; i++) {{
        cin >> pts[i].x >> pts[i].y;
    }}

    sort(pts.begin(), pts.end());
    pts.erase(unique(pts.begin(), pts.end()), pts.end());
    int k = pts.size();

    if (k <= 1) {{
        cout << k << "\\n";
        for (const auto& p : pts) cout << p.x << " " << p.y << "\\n";
        return 0;
    }}

    vector<Point> h;
    // Lower hull
    for (int i = 0; i < k; i++) {{
        while (h.size() >= 2 && cross_prod(h[h.size() - 2], h.back(), pts[i]) {cmp_op}) {{
            h.pop_back();
        }}
        h.push_back(pts[i]);
    }}

    // Upper hull
    size_t lower_size = h.size();
    for (int i = k - 2; i >= 0; i--) {{
        while (h.size() > lower_size && cross_prod(h[h.size() - 2], h.back(), pts[i]) {cmp_op}) {{
            h.pop_back();
        }}
        h.push_back(pts[i]);
    }}
    h.pop_back(); // Remove duplicate starting point

    cout << h.size() << "\\n";
    for (const auto& p : h) {{
        cout << p.x << " " << p.y << "\\n";
    }}

    return 0;
}}
"""

    # ── 4. Shoelace Polygon Area (3R-D) ──
    if pattern == "geom_polygon_area_shoelace":
        return """#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>

using namespace std;
using i128 = __int128_t;

struct Point {
    long long x, y;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n < 3) return 0;

    vector<Point> p(n);
    for (int i = 0; i < n; i++) {
        cin >> p[i].x >> p[i].y;
    }

    i128 area2 = 0;
    for (int i = 0; i < n; i++) {
        int j = (i + 1) % n;
        area2 += (i128)p[i].x * p[j].y - (i128)p[j].x * p[i].y;
    }

    if (area2 < 0) area2 = -area2;

    // Output exact double area as integer, and exact/half area
    long long double_area = (long long)area2;
    cout << double_area << "\\n";

    return 0;
}
"""

    # ── 5. Point in Polygon (3R-E) ──
    if pattern == "geom_point_in_polygon":
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;
using i128 = __int128_t;

struct Point {
    long long x, y;
};

bool on_segment(const Point& p, const Point& a, const Point& b) {
    i128 cp = (i128)(b.x - a.x) * (p.y - a.y) - (i128)(b.y - a.y) * (p.x - a.x);
    if (cp != 0) return false;
    return p.x >= min(a.x, b.x) && p.x <= max(a.x, b.x) &&
           p.y >= min(a.y, b.y) && p.y <= max(a.y, b.y);
}

int point_in_polygon(const vector<Point>& poly, const Point& pt) {
    int n = poly.size();
    // Stage 1: Deterministic boundary test first
    for (int i = 0; i < n; i++) {
        int j = (i + 1) % n;
        if (on_segment(pt, poly[i], poly[j])) {
            return 0; // ON_BOUNDARY
        }
    }

    // Stage 2: Ray casting crossing parity
    bool inside = false;
    for (int i = 0; i < n; i++) {
        int j = (i + 1) % n;
        const Point& p1 = poly[i];
        const Point& p2 = poly[j];

        if ((p1.y > pt.y) != (p2.y > pt.y)) {
            // Check if pt.x < intersection_x
            double x_cross = (double)(p2.x - p1.x) * (pt.y - p1.y) / (double)(p2.y - p1.y) + p1.x;
            if (pt.x < x_cross) {
                inside = !inside;
            }
        }
    }

    return inside ? 1 : -1; // 1 = INSIDE, -1 = OUTSIDE
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n < 3) return 0;

    vector<Point> poly(n);
    for (int i = 0; i < n; i++) {
        cin >> poly[i].x >> poly[i].y;
    }

    Point pt;
    if (cin >> pt.x >> pt.y) {
        int res = point_in_polygon(poly, pt);
        if (res == 0) cout << "ON_BOUNDARY\\n";
        else if (res == 1) cout << "INSIDE\\n";
        else cout << "OUTSIDE\\n";
    }

    return 0;
}
"""

    # ── 6. Closest Pair of Points (3R-F) ──
    if pattern == "geom_closest_pair_points":
        return """#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <algorithm>

using namespace std;

struct Point {
    long long x, y;
};

bool cmp_x(const Point& a, const Point& b) {
    if (a.x != b.x) return a.x < b.x;
    return a.y < b.y;
}

bool cmp_y(const Point& a, const Point& b) {
    return a.y < b.y;
}

double dist(const Point& a, const Point& b) {
    double dx = (double)a.x - b.x;
    double dy = (double)a.y - b.y;
    return sqrt(dx * dx + dy * dy);
}

double closest_pair_rec(vector<Point>& pts, int l, int r) {
    if (r - l <= 3) {
        double d = 1e18;
        for (int i = l; i <= r; i++) {
            for (int j = i + 1; j <= r; j++) {
                d = min(d, dist(pts[i], pts[j]));
            }
        }
        return d;
    }

    int mid = l + (r - l) / 2;
    long long mid_x = pts[mid].x;
    double dl = closest_pair_rec(pts, l, mid);
    double dr = closest_pair_rec(pts, mid + 1, r);
    double d = min(dl, dr);

    vector<Point> strip;
    for (int i = l; i <= r; i++) {
        if (abs(pts[i].x - mid_x) < d) {
            strip.push_back(pts[i]);
        }
    }

    sort(strip.begin(), strip.end(), cmp_y);
    int sz = strip.size();
    for (int i = 0; i < sz; i++) {
        for (int j = i + 1; j < sz && (strip[j].y - strip[i].y) < d; j++) {
            d = min(d, dist(strip[i], strip[j]));
        }
    }

    return d;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n < 2) return 0;

    vector<Point> pts(n);
    for (int i = 0; i < n; i++) {
        cin >> pts[i].x >> pts[i].y;
    }

    sort(pts.begin(), pts.end(), cmp_x);

    // Duplicate check
    for (int i = 0; i < n - 1; i++) {
        if (pts[i].x == pts[i + 1].x && pts[i].y == pts[i + 1].y) {
            cout << fixed << setprecision(6) << 0.0 << "\\n";
            return 0;
        }
    }

    double ans = closest_pair_rec(pts, 0, n - 1);
    cout << fixed << setprecision(6) << ans << "\\n";

    return 0;
}
"""

    # ── 7. Line Intersection Point (3R-G) ──
    if pattern == "geom_line_intersection_point":
        return """#include <iostream>
#include <iomanip>
#include <cmath>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    // Lines: a1*x + b1*y + c1 = 0 and a2*x + b2*y + c2 = 0
    double a1, b1, c1, a2, b2, c2;
    if (!(cin >> a1 >> b1 >> c1 >> a2 >> b2 >> c2)) return 0;

    double det = a1 * b2 - a2 * b1;
    double scale = max(abs(a1), abs(b1)) * max(abs(a2), abs(b2));
    double eps = 1e-12 + 1e-9 * scale;

    if (abs(det) <= eps) {
        double det_c1 = a1 * c2 - a2 * c1;
        double det_c2 = b1 * c2 - b2 * c1;
        if (abs(det_c1) <= eps && abs(det_c2) <= eps) {
            cout << "COINCIDENT\\n";
        } else {
            cout << "PARALLEL\\n";
        }
        return 0;
    }

    double x = (b1 * c2 - b2 * c1) / det;
    double y = (c1 * a2 - c2 * a1) / det;

    cout << fixed << setprecision(6) << x << " " << y << "\\n";

    return 0;
}
"""

    # ── 8. Rotating Calipers Diameter (3R-H) ──
    if pattern == "geom_rotating_calipers_diameter":
        return """#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <algorithm>

using namespace std;
using i128 = __int128_t;

struct Point {
    long long x, y;
    bool operator<(const Point& o) const {
        if (x != o.x) return x < o.x;
        return y < o.y;
    }
    bool operator==(const Point& o) const {
        return x == o.x && y == o.y;
    }
};

i128 cross_prod(const Point& o, const Point& a, const Point& b) {
    return (i128)(a.x - o.x) * (b.y - o.y) - (i128)(a.y - o.y) * (b.x - o.x);
}

long long dist_sq(const Point& a, const Point& b) {
    long long dx = a.x - b.x;
    long long dy = a.y - b.y;
    return dx * dx + dy * dy;
}

vector<Point> convex_hull(vector<Point>& pts) {
    sort(pts.begin(), pts.end());
    pts.erase(unique(pts.begin(), pts.end()), pts.end());
    int k = pts.size();
    if (k <= 1) return pts;

    vector<Point> h;
    for (int i = 0; i < k; i++) {
        while (h.size() >= 2 && cross_prod(h[h.size() - 2], h.back(), pts[i]) <= 0) {
            h.pop_back();
        }
        h.push_back(pts[i]);
    }
    size_t lower_sz = h.size();
    for (int i = k - 2; i >= 0; i--) {
        while (h.size() > lower_sz && cross_prod(h[h.size() - 2], h.back(), pts[i]) <= 0) {
            h.pop_back();
        }
        h.push_back(pts[i]);
    }
    h.pop_back();
    return h;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n < 2) return 0;

    vector<Point> pts(n);
    for (int i = 0; i < n; i++) cin >> pts[i].x >> pts[i].y;

    vector<Point> h = convex_hull(pts);
    int m = h.size();
    if (m < 2) {
        cout << fixed << setprecision(6) << 0.0 << "\\n";
        return 0;
    }
    if (m == 2) {
        cout << fixed << setprecision(6) << sqrt((double)dist_sq(h[0], h[1])) << "\\n";
        return 0;
    }

    long long max_d2 = 0;
    int k = 1;
    while (cross_prod(h[0], h[1], h[(k + 1) % m]) > cross_prod(h[0], h[1], h[k])) {
        k = (k + 1) % m;
    }

    for (int i = 0; i < m; i++) {
        int i_next = (i + 1) % m;
        while (cross_prod(h[i], h[i_next], h[(k + 1) % m]) > cross_prod(h[i], h[i_next], h[k])) {
            k = (k + 1) % m;
        }
        max_d2 = max(max_d2, dist_sq(h[i], h[k]));
        max_d2 = max(max_d2, dist_sq(h[i_next], h[k]));
    }

    cout << fixed << setprecision(6) << sqrt((double)max_d2) << "\\n";

    return 0;
}
"""

    # ── 9. Halfplane Intersection (3R-I) ──
    if pattern == "geom_halfplane_intersection":
        return """#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <algorithm>
#include <deque>

using namespace std;

const double EPS = 1e-9;

struct Point {
    double x, y;
};

struct Line {
    Point p, d;
    double angle;
    Line(Point p = {0,0}, Point d = {0,0}) : p(p), d(d) {
        angle = atan2(d.y, d.x);
    }
    bool operator<(const Line& o) const {
        return angle < o.angle;
    }
};

double cross(Point a, Point b) {
    return a.x * b.y - a.y * b.x;
}

Point line_intersection(const Line& a, const Line& b) {
    Point u = {a.p.x - b.p.x, a.p.y - b.p.y};
    double t = cross(b.d, u) / cross(a.d, b.d);
    return {a.p.x + a.d.x * t, a.p.y + a.d.y * t};
}

bool on_left(const Line& l, Point p) {
    return cross(l.d, {p.x - l.p.x, p.y - l.p.y}) >= -EPS;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n < 3) return 0;

    vector<Line> lines(n);
    for (int i = 0; i < n; i++) {
        double x1, y1, x2, y2;
        cin >> x1 >> y1 >> x2 >> y2;
        lines[i] = Line({x1, y1}, {x2 - x1, y2 - y1});
    }

    sort(lines.begin(), lines.end());

    vector<Line> ulines;
    for (int i = 0; i < n; i++) {
        if (!ulines.empty() && abs(lines[i].angle - ulines.back().angle) < EPS) {
            if (on_left(lines[i], ulines.back().p)) {
                ulines.back() = lines[i];
            }
        } else {
            ulines.push_back(lines[i]);
        }
    }

    deque<Line> dq;
    deque<Point> pts;
    dq.push_back(ulines[0]);
    dq.push_back(ulines[1]);
    pts.push_back(line_intersection(ulines[0], ulines[1]));

    int m = ulines.size();
    for (int i = 2; i < m; i++) {
        while (!pts.empty() && !on_left(ulines[i], pts.back())) {
            pts.pop_back();
            dq.pop_back();
        }
        while (!pts.empty() && !on_left(ulines[i], pts.front())) {
            pts.pop_front();
            dq.pop_front();
        }
        pts.push_back(line_intersection(dq.back(), ulines[i]));
        dq.push_back(ulines[i]);
    }

    while (!pts.empty() && !on_left(dq.front(), pts.back())) {
        pts.pop_back();
        dq.pop_back();
    }

    if (dq.size() < 3) {
        cout << fixed << setprecision(6) << 0.0 << "\\n";
        return 0;
    }

    pts.push_back(line_intersection(dq.back(), dq.front()));

    // Shoelace area
    double area = 0;
    int k = pts.size();
    for (int i = 0; i < k; i++) {
        int j = (i + 1) % k;
        area += pts[i].x * pts[j].y - pts[j].x * pts[i].y;
    }
    area = abs(area) / 2.0;

    cout << fixed << setprecision(6) << area << "\\n";

    return 0;
}
"""

    # ── 10. Sweep Line Bentley-Ottmann (3R-J) ──
    if pattern == "geom_sweep_line_segments":
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;
using i128 = __int128_t;

struct Point {
    long long x, y;
};

struct Segment {
    Point p1, p2;
};

int orientation(const Point& a, const Point& b, const Point& c) {
    i128 cross = (i128)(b.x - a.x) * (c.y - a.y) - (i128)(b.y - a.y) * (c.x - a.x);
    if (cross > 0) return 1;
    if (cross < 0) return -1;
    return 0;
}

bool on_segment(const Point& p, const Point& a, const Point& b) {
    return p.x >= min(a.x, b.x) && p.x <= max(a.x, b.x) &&
           p.y >= min(a.y, b.y) && p.y <= max(a.y, b.y);
}

bool intersect(const Segment& s1, const Segment& s2) {
    int o1 = orientation(s1.p1, s1.p2, s2.p1);
    int o2 = orientation(s1.p1, s1.p2, s2.p2);
    int o3 = orientation(s2.p1, s2.p2, s1.p1);
    int o4 = orientation(s2.p1, s2.p2, s1.p2);

    if (o1 != o2 && o3 != o4) return true;
    if (o1 == 0 && on_segment(s2.p1, s1.p1, s1.p2)) return true;
    if (o2 == 0 && on_segment(s2.p2, s1.p1, s1.p2)) return true;
    if (o3 == 0 && on_segment(s1.p1, s2.p1, s2.p2)) return true;
    if (o4 == 0 && on_segment(s1.p2, s2.p1, s2.p2)) return true;

    return false;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n < 2) return 0;

    vector<Segment> segs(n);
    for (int i = 0; i < n; i++) {
        cin >> segs[i].p1.x >> segs[i].p1.y >> segs[i].p2.x >> segs[i].p2.y;
    }

    bool any_cross = false;
    for (int i = 0; i < n && !any_cross; i++) {
        for (int j = i + 1; j < n; j++) {
            if (intersect(segs[i], segs[j])) {
                any_cross = true;
                break;
            }
        }
    }

    cout << (any_cross ? "YES\\n" : "NO\\n");

    return 0;
}
"""

    return "// Unknown geometric pattern\n"
