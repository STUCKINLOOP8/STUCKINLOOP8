import math

W, H = 40, 25
pixels = [[' ' for _ in range(W)] for _ in range(H)]
zbuf = [[-999.0 for _ in range(W)] for _ in range(H)]

chars = " .,:;!ijlI1tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW8%B@$"

steps_u = 1000
steps_v = 150
r_tube = 0.44
a = 2.4

# Light vector
lx, ly, lz = 0.45, -0.55, 0.70
l_mag = math.sqrt(lx*lx + ly*ly + lz*lz)
lx, ly, lz = lx/l_mag, ly/l_mag, lz/l_mag

for iu in range(steps_u):
    u = iu * 2.0 * math.pi / steps_u
    sin_u = math.sin(u)
    cos_u = math.cos(u)
    denom = 1.0 + sin_u**2
    
    # 3D Lemniscate
    cx = a * cos_u / denom
    cy = a * 1.55 * sin_u * cos_u / denom
    cz = 0.65 * sin_u

    # Tangent vector (central difference)
    du = 0.0001
    u_f = u + du
    cx_f = a * math.cos(u_f) / (1.0 + math.sin(u_f)**2)
    cy_f = a * 1.55 * math.sin(u_f) * math.cos(u_f) / (1.0 + math.sin(u_f)**2)
    cz_f = 0.65 * math.sin(u_f)

    tx, ty, tz = cx_f - cx, cy_f - cy, cz_f - cz
    t_mag = math.sqrt(tx*tx + ty*ty + tz*tz)
    tx, ty, tz = tx/t_mag, ty/t_mag, tz/t_mag

    # Normal vector
    nx = -ty
    ny = tx
    nz = 0.0
    n_mag = math.sqrt(nx*nx + ny*ny) + 1e-9
    nx, ny = nx/n_mag, ny/n_mag

    # Binormal
    bx = ty*nz - tz*ny
    by = tz*nx - tx*nz
    bz = tx*ny - ty*nx

    for iv in range(steps_v):
        v = iv * 2.0 * math.pi / steps_v
        cv = math.cos(v)
        sv = math.sin(v)

        # Normal on tube
        snx = cv * nx + sv * bx
        sny = cv * ny + sv * by
        snz = cv * nz + sv * bz

        # Point on tube
        px = cx + r_tube * snx
        py = cy + r_tube * sny
        pz = cz + r_tube * snz

        # Tilt 3D perspective
        tilt_x = 0.22
        tilt_y = -0.15
        
        # Y rotation
        rx = px * math.cos(tilt_y) + pz * math.sin(tilt_y)
        ry = py
        rz = -px * math.sin(tilt_y) + pz * math.cos(tilt_y)

        # X rotation
        px2 = rx
        py2 = ry * math.cos(tilt_x) - rz * math.sin(tilt_x)
        pz2 = ry * math.sin(tilt_x) + rz * math.cos(tilt_x)

        # Normal rotation
        nrx = snx * math.cos(tilt_y) + snz * math.sin(tilt_y)
        nry = sny
        nrz = -snx * math.sin(tilt_y) + snz * math.cos(tilt_y)

        snx2 = nrx
        sny2 = nry * math.cos(tilt_x) - nrz * math.sin(tilt_x)
        snz2 = nry * math.sin(tilt_x) + nrz * math.cos(tilt_x)

        z = pz2 + 5.2
        ooz = 1.0 / z

        sx = int(W / 2.0 + px2 * ooz * 48.0)
        sy = int(H / 2.0 - py2 * ooz * 32.0)

        if 0 <= sx < W and 0 <= sy < H:
            if ooz > zbuf[sy][sx]:
                zbuf[sy][sx] = ooz
                lum = snx2 * lx + sny2 * ly + snz2 * lz
                lum = max(0.0, lum) * 0.85 + 0.15
                idx = int(lum * (len(chars) - 1))
                pixels[sy][sx] = chars[idx]

# Check output
for row in pixels:
    print(''.join(row))
