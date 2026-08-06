import pygame
import math

HOTSPOT_FILL_COLOR = (255, 0, 0, 70)
HOTSPOT_BORDER_COLOR = (255, 0, 0)
HOTSPOT_BORDER_WIDTH = 5

class Hotspot:
    def __init__(self, points, room_index, hotspot_type, reference_index):
        self.points = points
        self.room_index = room_index
        self.hotspot_type = hotspot_type
        self.reference_index = reference_index

class PanoramaView:
    def __init__(self, room_actor, speed=6.4, slice_width=6, focal_length=1120):
        self.room_actor = room_actor
        self.speed = speed
        self.offset = 0
        self.slice_width = slice_width
        self.focal_length = focal_length

    def set_room_image(self, image_name):
        self.room_actor.image = image_name

    def move_left(self):
        self.offset -= self.speed

    def move_right(self):
        self.offset += self.speed

    def draw(self, screen):
        self.draw_cylindrical(screen)

    def draw_cylindrical(self, screen):
        panorama_surface = self.room_actor._surf
        screen_width = screen.surface.get_width()
        screen_height = screen.surface.get_height()
        panorama_width = panorama_surface.get_width()
        panorama_height = panorama_surface.get_height()
        screen_center_x = screen_width / 2

        # Schleife geht in slice_width Schritte von links (0) nach rechts (screen_width)
        # screen_x ist die linke Position eines Schnippsels
        for screen_x in range(0, screen_width, self.slice_width):
            # Falls es ganz rechts nicht aufgeht: statt 4 breit -> Bildschirmbreite - linke Postion des letzten Schnippsels
            current_slice_width = min(self.slice_width, screen_width - screen_x)

            # Für verzerrung braucht man die MItte des Schnippsels
            slice_center_x = screen_x + current_slice_width / 2

            # Berechnung wie weit der Schnippsel von der Mitte entfernt ist
            distance_from_center = slice_center_x - screen_center_x

            # Berechnung der Blickwinkels für eine zylinderische Projektion
            # Formel von ChatGPT
            view_angle = math.atan(distance_from_center / self.focal_length)

            # Blickwinkel wieder in "Panorama-Distanz" umrechenen
            projected_distance = view_angle * self.focal_length

            # Horizontale Stelle des aktuellen Schnippsels
            # int wird gebraucht um die Kommastellen zu entfernen und % panorama_width für endloses scrolen
            source_x = int((self.offset + screen_center_x + projected_distance) % panorama_width)

            # Falls ein Streifen rechts über den Bildschirmrand herausgeht, soll links das restliche Stück erscheinen
            source_width = min(current_slice_width, panorama_width - source_x)
            source_slice = pygame.Surface((current_slice_width, panorama_height)) # erstellt lehren Schnippsel
            first_source_slice = panorama_surface.subsurface((source_x, 0, source_width, panorama_height))
            source_slice.blit(first_source_slice, (0, 0))
            remaining_source_width = current_slice_width - source_width # normalesrweise geht es auf 4 - 4 = 0
            if remaining_source_width > 0: # falls nicht wird subsurface bei posiotn 0,0 (ganz links) eingefügt
                second_source_slice = panorama_surface.subsurface((0, 0, remaining_source_width, panorama_height))
                source_slice.blit(second_source_slice, (source_width, 0))

            # Schnippsel an der richtigen Stelle zeichenen
            screen.surface.blit(source_slice, (screen_x, 0))

    # Für Hotspots muss Panorama.x in Bildschirm.x umgerechnet werden§
    def world_x_to_screen_x(self, world_x, screen_width):
        panorama_width = self.room_actor._surf.get_width()
        screen_center_x = screen_width / 2

        # Welches Panorama.x sich in der Mitte befindet
        # Horizontaler Abstand von Hotspotpunkt und Mitte
        view_center_x = (self.offset + screen_center_x) % panorama_width
        wrapped_distance = (world_x - view_center_x + panorama_width / 2) % panorama_width
        wrapped_distance -= panorama_width / 2

        # Formel von ChatGPT
        view_angle = wrapped_distance / self.focal_length
        distance_from_center = math.tan(view_angle) * self.focal_length
        return distance_from_center + screen_center_x # Absolute Position

    def project_polygon(self, points, screen_width):
        projected_points = []

        for world_x, world_y in points:
            screen_x = self.world_x_to_screen_x(world_x, screen_width)
            projected_points.append((screen_x, world_y))
        if not projected_points:
            return projected_points

        unwrapped_points = [projected_points[0]]

        # Falls der Punkt mehr als eine halbe Bildschirmbreite entfernnt liegt, wird eh heran geschoben
        for screen_x, screen_y in projected_points[1:]:
            previous_x = unwrapped_points[-1][0]
            while screen_x - previous_x > screen_width / 2:
                screen_x -= screen_width
            while screen_x - previous_x < -screen_width / 2:
                screen_x += screen_width
            unwrapped_points.append((screen_x, screen_y))
        return unwrapped_points

def point_in_polygon(point, polygon):
    point_x, point_y = point
    inside = False
    previous_x, previous_y = polygon[-1]

    # Sogenanntes Ray-Casting-Verfahren (Idee von ChatGPT)
    # Wenn vom Mauspunkt eine Linie nach rechts gezogen wird und diese
    # gerade Anzahl Kollisionen mit Polygonlinien hat: ausserhalb
    # ungerade Anzahl Kollisionen Polygonlinien hat: innerhalb
    for current_x, current_y in polygon:
        edge_crosses_y = (current_y > point_y) != (previous_y > point_y)
        if edge_crosses_y:
            edge_width = previous_x - current_x
            edge_height = previous_y - current_y
            intersection_x = current_x + (point_y - current_y) * edge_width / edge_height
            if point_x < intersection_x:
                inside = not inside
        previous_x, previous_y = current_x, current_y
    return inside

def project_hotspot(hotspot, screen_width, panorama_view):
    return panorama_view.project_polygon(hotspot.points, screen_width)

def find_hotspot_at_point(point, room_index, hotspots, panorama_view, screen_width, hotspot_type=None):
    for hotspot in hotspots:
        if hotspot.room_index != room_index:
            continue
        if hotspot_type is not None and hotspot.hotspot_type != hotspot_type:
            continue

        polygon = project_hotspot(hotspot, screen_width, panorama_view)
        if point_in_polygon(point, polygon):
            return hotspot
    return None

def draw_hotspot_overlay(screen, room_index, active_hotspot, show_hotspot_debug, hotspots, panorama_view):
    overlay = pygame.Surface((screen.surface.get_width(), screen.surface.get_height()), pygame.SRCALPHA) #SRCALPHA (Transparent)
    visible_hotspots = []
    for hotspot in hotspots:
        if hotspot.room_index != room_index:
            continue
        if show_hotspot_debug or hotspot == active_hotspot:
            visible_hotspots.append(hotspot)

    for hotspot in visible_hotspots:
        polygon = project_hotspot(hotspot, screen.surface.get_width(), panorama_view)
        drawable_polygon = [(int(point_x), int(point_y)) for point_x, point_y in polygon]
        pygame.draw.polygon(overlay, HOTSPOT_FILL_COLOR, drawable_polygon)
        pygame.draw.polygon(overlay, HOTSPOT_BORDER_COLOR, drawable_polygon, HOTSPOT_BORDER_WIDTH)

    screen.surface.blit(overlay, (0, 0))
