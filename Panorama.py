import pygame

HOTSPOT_FILL_COLOR = (255, 0, 0, 70)
HOTSPOT_BORDER_COLOR = (255, 0, 0)
HOTSPOT_BORDER_WIDTH = 3


class Hotspot:
    def __init__(self, points, room_index, hotspot_type, reference_index):
        self.points = points
        self.room_index = room_index
        self.hotspot_type = hotspot_type
        self.reference_index = reference_index


class PanoramaView:
    def __init__(
        self,
        room_actor,
        speed=5,
        slice_width=4,
        focal_length=700,
        projection_strength=1.0,
        projection_mode="cylindrical"
    ):
        self.room_actor = room_actor
        self.speed = speed
        self.offset = 0
        self.slice_width = slice_width
        self.focal_length = focal_length
        self.projection_strength = projection_strength
        self.projection_mode = projection_mode
        self.linear_projection_mode = "linear"
        self.cylindrical_projection_mode = "cylindrical"

    def move_left(self):
        self.offset -= self.speed

    def move_right(self):
        self.offset += self.speed

    def draw(self, screen):
        if self.projection_mode == self.linear_projection_mode:
            self.draw_linear(screen)
        else:
            self.draw_cylindrical(screen)

    def draw_cylindrical(self, screen):
        import math

        panorama_surface = self.room_actor._surf
        screen_width = screen.surface.get_width()
        screen_height = screen.surface.get_height()
        panorama_width = panorama_surface.get_width()
        panorama_height = panorama_surface.get_height()
        screen_center_x = screen_width / 2

        for screen_x in range(0, screen_width, self.slice_width):
            current_slice_width = min(self.slice_width, screen_width - screen_x)

            # Each destination slice is represented by its horizontal center.
            # Using the center avoids sampling only the left edge of a slice,
            # which would make wide slices look slightly shifted.
            slice_center_x = screen_x + current_slice_width / 2

            # Measure how far the current screen slice is away from the center
            # of the visible image. A value of 0 means "straight ahead".
            distance_from_center = slice_center_x - screen_center_x

            # Convert the flat screen distance into a viewing angle. atan()
            # bends the mapping gently: slices near the center stay almost
            # unchanged, while slices near the edges are sampled differently.
            # This is the rough cylindrical part of the prototype.
            view_angle = math.atan(distance_from_center / self.focal_length)

            # Convert the angle back into a source offset inside the panorama.
            # projection_strength is intentionally exposed as a parameter so
            # the visual effect can be made weaker or stronger later without
            # changing the algorithm itself.
            projected_distance = view_angle * self.focal_length * self.projection_strength

            # Add the existing panorama offset so movement with A/D keeps
            # behaving like before. Modulo wraps around the single panorama
            # image, so no extra image files or pre-cut assets are needed.
            source_x = int((self.offset + screen_center_x + projected_distance) % panorama_width)

            # Cut one narrow vertical strip from the original panorama at
            # runtime. If a strip crosses the right edge of the panorama, copy
            # the first part from the right edge and the missing part from the
            # left edge. This preserves the endless 360-degree wrap-around.
            source_width = min(current_slice_width, panorama_width - source_x)
            source_slice = pygame.Surface((current_slice_width, panorama_height))
            first_source_slice = panorama_surface.subsurface((source_x, 0, source_width, panorama_height))
            source_slice.blit(first_source_slice, (0, 0))
            remaining_source_width = current_slice_width - source_width
            if remaining_source_width > 0:
                second_source_slice = panorama_surface.subsurface((0, 0, remaining_source_width, panorama_height))
                source_slice.blit(second_source_slice, (source_width, 0))

            # Draw the sampled strip into the current screen position. Scaling
            # keeps the result usable even if the source panorama and the game
            # window do not have exactly the same height.
            scaled_slice = pygame.transform.scale(source_slice, (current_slice_width, screen_height))
            screen.surface.blit(scaled_slice, (screen_x, 0))

    def draw_linear(self, screen):
        screen.blit(self.room_actor.image, (0 - self.offset, 0))
        screen.blit(self.room_actor.image, (self.room_actor.width - self.offset, 0))

    def world_x_to_screen_x(self, world_x, screen_width):
        import math

        panorama_width = self.room_actor._surf.get_width()
        screen_center_x = screen_width / 2

        # draw_cylindrical() maps a screen position to a panorama x-position.
        # For polygon hotspots we need the inverse: start with a panorama
        # x-position, measure its wrapped distance from the current view center,
        # then undo the angle calculation used by the cylindrical projection.
        view_center_x = (self.offset + screen_center_x) % panorama_width
        wrapped_distance = (world_x - view_center_x + panorama_width / 2) % panorama_width
        wrapped_distance -= panorama_width / 2

        # This reverses:
        # projected_distance = view_angle * focal_length * projection_strength
        # distance_from_center = tan(view_angle) * focal_length
        view_angle = wrapped_distance / (self.focal_length * self.projection_strength)
        distance_from_center = math.tan(view_angle) * self.focal_length
        return screen_center_x + distance_from_center

    def project_polygon(self, points, screen_width):
        # Points are stored in panorama coordinates. Only x is projected because
        # the current panorama projection bends horizontally; y remains in the
        # same internal game coordinate system as before.
        projected_points = []
        for world_x, world_y in points:
            screen_x = self.world_x_to_screen_x(world_x, screen_width)
            projected_points.append((screen_x, world_y))
        return projected_points


def point_in_polygon(point, polygon):
    point_x, point_y = point
    inside = False
    previous_x, previous_y = polygon[-1]

    # Ray casting: draw an imaginary horizontal ray from the mouse position to
    # the right. Every time the ray crosses a polygon edge, inside/outside
    # toggles. An odd number of crossings means the point is inside.
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

        # Mouse positions are already converted back into internal game
        # coordinates. The hotspot polygon is projected into those same screen
        # coordinates before the point-in-polygon test runs.
        polygon = project_hotspot(hotspot, screen_width, panorama_view)
        if point_in_polygon(point, polygon):
            return hotspot
    return None


def draw_hotspot_overlay(screen, room_index, active_hotspot, show_hotspot_debug, hotspots, panorama_view):
    overlay = pygame.Surface((screen.surface.get_width(), screen.surface.get_height()), pygame.SRCALPHA)
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
