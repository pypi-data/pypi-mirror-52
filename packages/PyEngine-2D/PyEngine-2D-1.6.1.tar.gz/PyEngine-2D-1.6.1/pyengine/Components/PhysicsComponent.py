import math

import pymunk

from pyengine.Components.PositionComponent import PositionComponent
from pyengine.Components.SpriteComponent import SpriteComponent
from pyengine.Utils.Vec2 import Vec2

__all__ = ["PhysicsComponent"]


class PhysicsComponent:
    def __init__(self, affectbygravity: bool = True, friction: float = .5, elasticity: float = .5, mass: int = 1,
                 solid: bool = True, can_rot: bool = True, callback=None):
        self.__entity = None
        self.orig_image = None
        self.body = None
        self.shape = None
        self.__affectbygravity = affectbygravity
        self.__friction = friction
        self.__elasticity = elasticity
        self.__mass = mass
        self.can_rot = can_rot
        self.solid = solid
        self.callback = callback

    @property
    def affectbygravity(self):
        return self.__affectbygravity

    @affectbygravity.setter
    def affectbygravity(self, val):
        if val:
            self.body.body_type = self.body.DYNAMIC
        else:
            self.body.body_type = self.body.KINEMATIC
        self.__affectbygravity = val

    @property
    def friction(self):
        return self.__friction

    @friction.setter
    def friction(self, val):
        self.shape.friction = val
        self.__friction = val

    @property
    def elasticity(self):
        return self.__elasticity

    @elasticity.setter
    def elasticity(self, val):
        self.shape.elasticity = val
        self.__elasticity = val

    @property
    def mass(self):
        return self.__mass

    @mass.setter
    def mass(self, val):
        moment = pymunk.moment_for_box(self.mass, (self.entity.rect.width, self.entity.rect.height))
        self.body = pymunk.Body(self.mass, moment)
        self.body.center_of_gravity = (self.entity.rect.width/2, self.entity.rect.height/2)
        self.shape.body = self.body

    @property
    def entity(self):
        return self.__entity

    @entity.setter
    def entity(self, entity):
        self.__entity = entity
        self.orig_image = entity.image
        if self.entity.has_component(SpriteComponent):
            temp = self.entity.get_component(SpriteComponent).origin_image.get_rect()
            temp2 = temp.height/2
            temp = temp.width/2
        else:
            temp = entity.rect.width/2
            temp2 = entity.rect.height/2
        vc = [(-temp, -temp2), (temp, -temp2), (-temp, temp2), (temp, temp2)]
        moment = pymunk.moment_for_box(self.mass, (temp*2, temp2*2))
        self.body = pymunk.Body(self.mass, moment)
        if not self.affectbygravity:
            self.body.body_type = self.body.KINEMATIC
        self.shape = pymunk.Poly(self.body, vc)
        self.shape.friction = self.friction
        self.shape.elasticity = self.elasticity
        if self.entity.has_component(SpriteComponent):
            self.update_rot(self.entity.get_component(SpriteComponent).rotation)

    def flipy(self, pos):
        return [pos[0], -pos[1] + self.entity.system.world.window.height]

    def update(self):
        if not self.can_rot:
            self.body.angular_velocity = 0
            self.body.angle = 0

        if self.entity.has_component(PositionComponent):
            if str(self.body.position[0]) != "nan" and str(self.body.position[1]) != "nan": 
                pos = Vec2(self.flipy(self.body.position))
                self.entity.get_component(PositionComponent).position = pos
            
        if self.entity.has_component(SpriteComponent):
            self.entity.get_component(SpriteComponent).make_rotation(math.degrees(self.body.angle))

    def update_pos(self, pos):
        self.body.position = self.flipy(pos)

    def update_rot(self, rot):
        self.body.angle = math.radians(rot)

    def check_grounding(self):
        """ See if the player is on the ground. Used to see if we can jump. """
        grounding = {
            'normal': pymunk.Vec2d.zero(),
            'penetration': pymunk.Vec2d.zero(),
            'impulse': pymunk.Vec2d.zero(),
            'position': pymunk.Vec2d.zero(),
            'body': None
        }

        def f(arbiter):
            n = -arbiter.contact_point_set.normal
            if n.y > grounding['normal'].y:
                grounding['normal'] = n
                grounding['penetration'] = -arbiter.contact_point_set.points[0].distance
                grounding['body'] = arbiter.shapes[1].body
                grounding['impulse'] = arbiter.total_impulse
                grounding['position'] = arbiter.contact_point_set.points[0].point_b

        self.body.each_arbiter(f)

        return grounding


