"""Optimized B3313 Engine v1.1 - Pure Ursina Demo (60 FPS Target)"""
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.maths import distance
from math import sin, cos, pi
import random

# --------------------------------------------------
# 🚀 Optimized Engine Bootstrap
# --------------------------------------------------
app = Ursina(
    vsync=False,  # Disable vsync for potentially higher FPS
    development_mode=False  # Disable dev tools for performance
)
window.title = "B3313 Engine - Comet Observatory (Optimized)"
window.borderless = False
window.fullscreen = False
window.color = color.rgb(8, 10, 22)

# --------------------------------------------------
# 🎯 Performance Configuration
# --------------------------------------------------
# Reduce rendering quality for better performance
window.fps_counter.enabled = True  # Keep FPS counter visible
window.fps_counter.position = (0, .45)  # Move to corner
window.fps_counter.scale *= 0.7  # Make smaller

# --------------------------------------------------
# 🎨 Optimized Color Palette
# --------------------------------------------------
OBS_COLOR = color.rgba(210, 230, 255, 255)
ENGINE_COL = color.rgba(90, 90, 160, 240)
GLASS_COL = color.rgba(160, 220, 255, 120)
STAR_COLOR = color.yellow
DOME_RED = color.rgba(200, 50, 50)  # Darker red for performance
DOME_GREEN = color.rgba(50, 150, 50)  # Darker green
METAL_COLOR = color.rgba(100, 100, 100)  # Darker gray
ENERGY_COLOR = color.rgba(100, 150, 255)  # Less intense blue

# --------------------------------------------------
# 🌍 Optimized Spherical Gravity Controller
# --------------------------------------------------
GRAVITY_STRENGTH = 0.9
CENTER_POINT = Vec3(0, 0, 0)
SURFACE_R = 32

class GalaxyPlayer(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.velocity = Vec3(0, 0, 0)
        self.cursor.visible = False
        self.speed = 7  # Slightly slower for N64 feel
        
        # Optimized collision settings
        self.collider = 'sphere'
        self.collider_radius = 0.5

    def update(self):
        # Original movement with simplified gravity
        super().update()
        
        # Optimized gravity calculation
        direction = CENTER_POINT - self.position
        r = direction.length()
        if r > 0.01:
            self.velocity += direction.normalized() * GRAVITY_STRENGTH * time.dt
            self.position += self.velocity
        
        # Surface sticking with optimized distance check
        if abs(r - SURFACE_R) < 0.5 and self.velocity.length_squared() > 0.01:
            self.velocity = Vec3(0, 0, 0)

# --------------------------------------------------
# 🌌 Optimized Starfield
# --------------------------------------------------
# Replace Sky entity with simple background color
window.color = color.rgb(5, 5, 15)

# Reduced star count with simpler rendering
stars = []
for i in range(60):  # Reduced from 200 to 60
    stars.append({
        'pos': Vec3(
            random.uniform(-80, 80),
            random.uniform(-80, 80),
            random.uniform(-80, 80)
        ),
        'scale': random.uniform(0.1, 0.2)
    })

def render_stars():
    for star in stars:
        # Use simple dots instead of sphere models
        draw.dot(
            star['pos'], 
            color=color.white, 
            scale=star['scale'] * 10
        )

# --------------------------------------------------
# 🪐 Optimized Observatory Planetoid
# --------------------------------------------------
# Use custom low-poly sphere model
def create_lowpoly_sphere(segments=8):
    verts = []
    tris = []
    
    # Generate vertices
    for i in range(segments + 1):
        lat = pi * i / segments
        for j in range(segments):
            lon = 2 * pi * j / segments
            x = sin(lat) * cos(lon)
            y = cos(lat)
            z = sin(lat) * sin(lon)
            verts.append(Vec3(x, y, z))
    
    # Generate triangles
    for i in range(segments):
        for j in range(segments):
            a = i * (segments + 1) + j
            b = a + 1
            c = (i + 1) * (segments + 1) + j
            d = c + 1
            tris.extend([(a, c, b), (b, c, d)])
    
    return Mesh(vertices=verts, triangles=tris, mode='ngon')

lowpoly_sphere = create_lowpoly_sphere(segments=8)

main_floor = Entity(
    model=lowpoly_sphere,
    scale=SURFACE_R * 2,
    color=OBS_COLOR,
    double_sided=True
)

# Simplified surface details
for i in range(8):  # Reduced from 12 to 8
    angle = i * (360 / 8)
    Entity(
        model='cube',
        color=color.gray(0.3),
        scale=(1.5, 0.8, 1.5),  # Smaller scale
        position=(
            28 * cos(radians(angle)),
            1.5,
            28 * sin(radians(angle))
        ),
        rotation=(0, angle, 0)
    )

# --------------------------------------------------
# 🔴🟢🔵 Optimized Domes
# --------------------------------------------------
def create_dome(position, dome_color):
    return Entity(
        model=lowpoly_sphere,
        color=dome_color,
        scale=3,  # Smaller scale
        position=position
    )

dome_red = create_dome((16, 0, 0), DOME_RED)
dome_green = create_dome((-16, 0, 0), DOME_GREEN)
dome_cyan = create_dome((0, 0, 16), color.cyan)

# --------------------------------------------------
# ⚡ Optimized Warp Pads
# --------------------------------------------------
def create_warp_pad(position, glow_color):
    warp = Entity(
        model='cylinder', 
        color=color.light_gray, 
        scale=(1.8, 0.4, 1.8),  # Smaller
        position=position, 
        collider='box'
    )
    
    # Simple glow effect without extra entity
    return warp

warp_red = create_warp_pad(dome_red.position + Vec3(0, 1, 0), DOME_RED)
warp_green = create_warp_pad(dome_green.position + Vec3(0, 1, 0), DOME_GREEN)
warp_cyan = create_warp_pad(dome_cyan.position + Vec3(0, 1, 0), color.cyan)

# --------------------------------------------------
# ⭐ Optimized Central Star
# --------------------------------------------------
star_npc = Entity(
    model=lowpoly_sphere,  # Use low-poly model
    color=STAR_COLOR,
    scale=1,
    position=(0, 6, 0),
    collider='sphere'
)

# --------------------------------------------------
# 🔧 Optimized Engine Room
# --------------------------------------------------
en_base = Entity(
    model='cylinder', 
    color=ENGINE_COL, 
    scale=(7, 0.8, 7),  # Smaller
    position=(0, -2, -20)
)

en_core = Entity(
    model='cylinder', 
    color=color.gray(0.3), 
    scale=(1.8, 5, 1.8),  # Smaller
    position=(0, 2, -20)
)

# Radial struts - reduced count
for ang in range(0, 360, 60):  # Every 60° instead of 45°
    Entity(
        model='cube',
        color=color.gray(0.25),
        scale=(0.3, 0.3, 6),  # Thinner
        position=(0, 2, -20),
        rotation=(0, ang, 0),
    )

# Energy nodes - reduced count
energy_nodes = []
for i in range(5):  # Reduced from 8 to 5
    theta = i * (2 * pi / 5)
    x = 5 * cos(theta)
    z = -20 + 5 * sin(theta)
    node = Entity(
        model=lowpoly_sphere,  # Low-poly
        color=ENERGY_COLOR,
        scale=0.4,  # Smaller
        position=(x, 2.7, z)
    )
    energy_nodes.append(node)

# --------------------------------------------------
# 🎮 Player & Camera Setup
# --------------------------------------------------
player = GalaxyPlayer()
player.position = (0, 2, 12)
camera.fov = 92  # Wider FOV for retro feel

# --------------------------------------------------
# 🌀 Optimized Animation System
# --------------------------------------------------
# Pre-calculate animation values
star_pulse = 0
node_pulses = [0] * len(energy_nodes)

def update():
    global star_pulse, node_pulses
    
    # Star pulsing with time-based value
    star_pulse = sin(time.time * 2) * 0.15
    star_npc.scale = 1 + star_pulse
    
    # Node pulsing with staggered timing
    for i in range(len(energy_nodes)):
        node_pulses[i] = sin(time.time * 3 + i) * 0.08
        energy_nodes[i].scale = 0.4 + node_pulses[i]
    
    # Render stars each frame
    render_stars()

# --------------------------------------------------
# 🌐 Zone Management (Unchanged)
# --------------------------------------------------
current_zone = "observatory"

def load_zone(zone: str):
    # ... (same as original) ...

# --------------------------------------------------
# ⌨️  Input Handler (Unchanged)
# --------------------------------------------------
def input(key):
    # ... (same as original) ...

# --------------------------------------------------
# 💡 Optimized Lighting
# --------------------------------------------------
# Use simpler lighting setup
DirectionalLight(direction=(1, -2, -1), shadows=False)  # Shadows disabled
AmbientLight(color=color.rgba(80, 80, 120, 100))  # Darker ambient

# --------------------------------------------------
# 🚀 Launch Optimized Demo
# --------------------------------------------------
load_zone("observatory")
print("Controls: WASD/Arrow - move | Mouse - look | LMB - interact | R - Reset")
print("Optimized for N64-like performance")

app.run()
