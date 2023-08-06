import pygame

from pyengine.Utils.Vec2 import Vec2

__all__ = ["PositionComponent"]


class PositionComponent:
    def __init__(self, position: Vec2, offset: Vec2 = Vec2()):
        self.__entity = None

        if not isinstance(position, pygame.Vector2):
            raise TypeError("Position must be a Vec2")
        if not isinstance(offset, pygame.Vector2):
            raise TypeError("Offset must be a Vec2")

        self.__offset = offset
        self.__position = position

    @property
    def entity(self):
        return self.__entity

    @entity.setter
    def entity(self, entity):
        self.__entity = entity
        self.update_dependances()

    @property
    def offset(self):
        return self.__offset

    @offset.setter
    def offset(self, val):
        if not isinstance(val, pygame.Vector2):
            raise TypeError("Offset must be a Vec2")

        self.__offset = val
        self.update_dependances()

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        if not isinstance(position, pygame.Vector2):
            raise TypeError("Position must be a Vec2")

        self.__position = position
        self.update_dependances()

    def update_phys(self):
        from pyengine.Components import PhysicsComponent

        if self.entity.has_component(PhysicsComponent):
            self.entity.get_component(PhysicsComponent).update_pos(self.position.coords)

    def update_dependances(self):
        from pyengine.Components import SpriteComponent, TextComponent  # Avoid import cycle

        if self.entity.has_component(SpriteComponent):
            self.entity.get_component(SpriteComponent).update_position()

        if self.entity.has_component(TextComponent):
            self.entity.get_component(TextComponent).update_position()

        for i in self.entity.attachedentities:
            if i.has_component(PositionComponent):
                i.get_component(PositionComponent).position = self.position
