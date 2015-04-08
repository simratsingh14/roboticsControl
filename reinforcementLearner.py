#!/usr/bin/env python

#approach based on the example from 'Reinforcement Learning: An Introduction' by Richard S. Sutton and Andrew G. Barto

class ReinforcementLearner():

  def __init__(self, controller):
    self.n_states = 162
    self.alpha = 1000     # learning rate for action weights
    self.beta = 0.5       # learning rate for critic weights
    self.gamma = 0.95     # discount factor for critic
    self.lambda_w = 0.9   # decay rate for w
    self.lambda_v = 0.8   # decay rate for v
    self.max_failures = 100
    self.max_steps = 1000000
    self.debug = 0

    self.one_degree = 0.0174532    # 2pi/360
    self.six_degrees = 0.1047192
    self.twelve_degrees = 0.2094384
    self.fifty_degrees = 0.87266

    self.max_distance = 2.4
    self.max_speed = 1
    self.max_angle = self.twelve_degrees

    self.w = [0] * self.n_states
    self.v = [0] * self.n_states
    self.e = [0] * self.n_states
    self.xbar = [0] * self.n_states

    #position, velocity, angle, angle velocity
    self.x, self.dx, self.t, self.dt = 0, 0, 0, 0

    self.controller = controller

  # matches the current state to an integer between 1 and n_states
  def get_state(self):
    state = 0

    # failed
    if self.x < -self.max_distance or self.x > self.max_distance or self.t < -self.max_angle or self.t > self.max_angle:
      return -1

    #position
    if self.x < -0.8:
      state = 0
    elif self.x < 0.8:
      state = 1
    else:
      state = 2

    #velocity
    if self.dx < -self.max_speed:
      state += 0
    elif self.dx < 0.5:
      state += 3
    else:
      state += 6

    #angle
    if self.t < -self.six_degrees:
      state += 0
    elif self.t < -self.one_degree:
      state += 9
    elif self.t < 0:
      state += 18
    elif self.t < self.one_degree:
      state += 27
    elif self.t < self.six_degrees:
      state += 36
    else:
      state += 45

    #angle velocity
    if self.dt < -self.fifty_degrees:
      state += 0
    elif self.dt < self.fifty_degrees:
      state += 54
    else:
      state += 108

    return state

  def read_variables(self):
    self.x = self.controller.get_current_position()[0]
    self.dx = self.controller.get_current_ground_speed()[0]
    self.t = self.controller.get_current_angle()[1]
    self.dt = self.controller.get_current_angle_speed()[1]

  # executes action and updates x, dx, t, dt
  def do_action(self, action):
    if action == True:
      self.controller.set_target_velocities(self.max_speed,self.max_speed)
    else:
      self.controller.set_target_velocities(-self.max_speed,-self.max_speed)