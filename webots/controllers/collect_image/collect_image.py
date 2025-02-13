#!/usr/bin/env python3

# Apache License
# Version 2.0, January 2004
# http://www.apache.org/licenses/
# Copyright 2024 Yasuo Hayashibara,Hiroki Noguchi,Satoshi Inoue

from controller import Robot
#from kinematics import *
from foot_step_planner import *
from preview_control import *
from walking import *
from ImageWriter import ImageWriter
from random import random 
#import walk_server
import time
import sys

class selfPosition:
  def __init__(self):
    self.x = 0.0
    self.y = 0.0
    self.theta = 0.0
  def update(self, x, y, theta):
    self.x += x
    self.y += y
    self.theta += theta

  def get_position(self):
    return round(self.x, 2), round(self.y, 2), round(self.theta, 2)

class Action:
    def __init__(self):
        self.base_move_dist = 0.1

    def turn_left(self):
        return 0, 0, self.base_move_dist
    def turn_right(self):
        return 0, 0, -self.base_move_dist
    def move_forward(self):
        return self.base_move_dist, 0, 0
    def move_backward(self):
        return -self.base_move_dist, 0, 0
    def move_left(self):
        return 0, self.base_move_dist, 0
    def move_right(self):
        return 0, -self.base_move_dist, 0

motorNames = [
  "head_yaw_joint",                        # ID1
  "left_shoulder_pitch_joint",             # ID2
  "left_shoulder_roll_joint",              # ID3
  "left_elbow_pitch_joint",                # ID4
  "right_shoulder_pitch_joint",            # ID5
  "right_shoulder_roll_joint",             # ID6
  "right_elbow_pitch_joint",               # ID7
  "left_waist_yaw_joint",                  # ID8
  "left_waist_roll_joint",                 # ID9
  "left_upper_knee_pitch_joint",                # ID10
  "left_knee_pitch_joint",                 # ID11
  "left_ankle_pitch_joint",                # ID12
  "left_ankle_roll_joint",                 # ID13
  "right_waist_yaw_joint",                 # ID14
  "right_waist_roll_joint",                # ID15
  "right_upper_knee_pitch_joint",               # ID16
  "right_knee_pitch_joint",                # ID17
  "right_ankle_pitch_joint",               # ID18
  "right_ankle_roll_joint"                 # ID19
]

if __name__ == '__main__':
  robot = Robot()
  timestep = int(robot.getBasicTimeStep())

  self_position = selfPosition()
  action = Action()

  move_y_threshold = 0.5
  close_ball_threshold = 0.5
  far_ball_threshold = 2.0

  walk_port = 7650
  camera_port = 8765
  print(f"check args {sys.argv[1]}, len: {len(sys.argv)}")
  if len(sys.argv) == 3:
    walk_port = int(sys.argv[1])
    camera_port = int(sys.argv[2])

  is_camera_sensor = False
  if camera_port == 8765:
    is_camera_sensor = True
    image_writer = ImageWriter(is_segmented_image=True)

  print(f"Walk server port: {walk_port}")
  print(f"Camera server port: {camera_port}")

  motor = [None]*len(motorNames)
  for i in range(len(motorNames)):
    motor[i] = robot.getDevice(motorNames[i])

  joint_angles = [0]*len(motorNames)

  print(f"joint_angles: {joint_angles}")

  left_foot  = [-0.02, +0.054, 0.02]
  right_foot = [-0.02, -0.054, 0.02]

  pc = preview_control(timestep/1000, 1.0, 0.27)
  walk = walking(timestep/1000, motorNames, left_foot, right_foot, joint_angles, pc)
  #walk_server = walk_server.WalkServer(walk_port, camera_port)
  if(is_camera_sensor):

      camera = robot.getDevice("camera_sensor")
      camera.enable(int(robot.getBasicTimeStep()))

      camera.recognitionEnable(timestep)
      camera.enableRecognitionSegmentation()

  time.sleep(2)
  camera_fps = 75
  loop_counter = 0

  camera_in_count = 0
  save_image_count = 0
  image_quality = 100

  #goal position (x, y) theta
  # foot_step = walk.setGoalPos([0.4, 0.0, 0.5])
  self_position.update(0.1, 0.0, 0.0)
  foot_step = walk.setGoalPos(self_position.get_position())
  command = None
  while robot.step(timestep) != -1:
    # receive command
    """
    if command is None:
      command = walk_server.getCommand()
      if command is not None:
        print("Received command...")
        print(command)
    """

    # send camera image
    loop_counter += 1
    command_is_updated = False
    if (loop_counter * timestep) > (1000 / camera_fps) and is_camera_sensor:
      img = np.frombuffer(camera.getImage(), dtype=np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
      #image = camera.getImage()

      width = camera.getWidth()
      height = camera.getHeight()
      #walk_server.sendImageData(width, height, image)
      
      recognition_image = np.frombuffer(camera.getRecognitionSegmentationImage(), dtype=np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))

      loop_counter = 0
      if(camera_in_count > camera_fps):
        image_writer.saveImage(img, recognition_image)
        camera_in_count = 0


        detect_object_num = camera.getRecognitionNumberOfObjects()
        detect_objects = camera.getRecognitionObjects()
        for i in range(detect_object_num):
          if detect_objects[i].getModel() == "soccer ball":
            command_is_updated = True
            ball_position_x, ball_position_y, ball_position_th = detect_objects[i].getPosition()
            print(f"Ball position: ({ball_position_x}, {ball_position_y}, {ball_position_th})")
            if(abs(ball_position_y) > move_y_threshold):
              if ball_position_x > 0.5:
                  if ball_position_y > 0:
                      command = action.turn_left()
                  else:
                      command = action.turn_right()
              else:
                  if ball_position_y > 0:
                      command = action.move_left()
                  else:
                      command = action.move_right()
            else:
              if ball_position_x > far_ball_threshold:
                  command = action.move_forward() * 5
              elif ball_position_x > close_ball_threshold:
                  command = action.move_forward() 
              elif ball_position_y > 0:
                  command = action.move_left()
              else:
                  command = action.move_right()
      camera_in_count += 1
    
    if command_is_updated:
        self_position.update(command[0], command[1], command[2])
        command = self_position.get_position()
        command_is_updated = False
    joint_angles,lf,rf,xp,n = walk.getNextPos()
    if n == 0:
      if command is not None:
        #x_goal, y_goal, th = command.target_x, command.target_y, command.target_theta
        x_goal, y_goal, th = command[0], command[1], command[2]
        print("Goal: ("+str(x_goal)+", "+str(y_goal)+", "+str(th)+")")
        foot_step = walk.setGoalPos([x_goal, y_goal, th])
        command = None
      else:
        foot_step = walk.setGoalPos()
    for i in range(len(motorNames)):
      motor[i].setPosition(joint_angles[i])
    pass

