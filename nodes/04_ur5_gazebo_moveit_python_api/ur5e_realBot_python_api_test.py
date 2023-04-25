#!/usr/bin/env python
# ur5e_realBot_python_api_test.py
# ------------------------------------
# edited WHS, OJ , 25.4.2023 #
# -------------------------------------
# Pick and Place
# in Python mit der move_group_api
# und Kollsionsverhütung
# -----------------------------------------
# basiert auf dem Code
# https://roboticscasual.com/ros-tutorial-pick-and-place-task-with-the-moveit-c-interface/
# -----------------------------------------
# usage
#   $1 real Robot und Moveit
# 
#   $2 rosrun THIS FILE
# ----------------------------------------------------------------
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
import numpy as np  # für deg2rad


def wait_for_state_update(box_name, scene, box_is_known=False,
                          box_is_attached=False, timeout=4):
    start = rospy.get_time()
    seconds = rospy.get_time()
    while (seconds - start < timeout) and not rospy.is_shutdown():
        attached_objects = scene.get_attached_objects([box_name])
        is_attached = len(attached_objects.keys()) > 0
        is_known = box_name in scene.get_known_object_names()
        if (box_is_attached == is_attached) and (box_is_known == is_known):
            return True
        rospy.sleep(0.1)
        seconds = rospy.get_time()
    return False


# First initialize moveit_ Command and rospy nodes:
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial',
                anonymous=True)
# Instantiate the robot commander object,
# which is used to control the whole robot
robot = moveit_commander.RobotCommander()

# Instantiate the MoveGroupCommander object.
group_name = "ur5_arm"
group = moveit_commander.MoveGroupCommander(group_name)
group_name_gripper = "gripper"
group_gripper = moveit_commander.MoveGroupCommander(group_name_gripper)

# Create a Publisher.
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                               moveit_msgs.msg.DisplayTrajectory,
                                               queue_size=20)

# ##### Getting Basic Information ###############
# We can get the name of the reference frame for this robot:
planning_frame = group.get_planning_frame()
print("= Reference frame: %s" % planning_frame)

# We can also print the name of the end-effector link for this group:
eef_link = group.get_end_effector_link()
print("= End effector: %s" % eef_link)

# We can get a list of all the groups in the robot:
group_names = robot.get_group_names()
print("= Robot Groups:", robot.get_group_names())

# Sometimes for debugging it is useful to print the entire state of the
# robot:
print("= Printing robot state")
print(robot.get_current_state())
print("")

# Create an Collision object for PlanningSceneInterface.
print("=== Adding Desktop-Plate to Planning Scene  ===")
scene = moveit_commander.PlanningSceneInterface()
rospy.sleep(2.0)
box_pose = geometry_msgs.msg.PoseStamped()
box_pose.header.frame_id = robot.get_planning_frame() 
box_pose.pose.orientation.w = 1.0
box_pose.pose.position.z = -0.2
box_name = "desktop"
scene.add_box(box_name, box_pose, size=(2.0, 2.0, 0.1))
rospy.loginfo(wait_for_state_update(box_name, scene, box_is_known=True))

# --- 1. Move the TCP above the Blue Lego
input(" Go to Blue Lego Position => Enter")
joint_goal = group.get_current_joint_values()
joint_goal[0] = np.deg2rad(36)       # shoulder pan
joint_goal[1] = np.deg2rad(-55)      # shoulder lift
joint_goal[2] = np.deg2rad(80)      # elbow
joint_goal[3] = np.deg2rad(-114)     # wrist1
joint_goal[4] = np.deg2rad(-91)     # wrist2
joint_goal[5] = np.deg2rad(38)      # wrist3
group.go(joint_goal, wait=True)
print("Reached Lego Position", joint_goal)

# --- 1a. Move the TCP above the Blue Lego 10cm up
input(" Move 30cm up => Enter")
# ============== Cartesian Paths ==============
print("plan a cartesion path")
# The Cartesian path is directly planned by specifying
# the waypoints list through which the end effector passes
waypoints = []
wpose = group.get_current_pose().pose
wpose.position.z = 0.5  # First move up (z)
wpose.position.y = -0.1  # First move up (z)
waypoints.append(copy.deepcopy(wpose))

# We want the Cartesian path to be interpolated at a resolution of 1 cm
# which is why we will specify 0.01 as the eef_step in Cartesian
# translation.  We will disable the jump threshold
# by setting it to 0.0 disabling:
(plan, fraction) = group.compute_cartesian_path(
                                                waypoints,
                                                0.01,        # eef_step
                                                0.0)         # jump_threshold
# Displaying a Trajectory
display_trajectory = moveit_msgs.msg.DisplayTrajectory()
display_trajectory.trajectory_start = robot.get_current_state()
display_trajectory.trajectory.append(plan)

# Publish
display_trajectory_publisher.publish(display_trajectory)

# ==== Execute the calculated path:
# print("the plan is", plan)
print("execute plan ")
group.execute(plan, wait=True)

"""# 1b Attaching box on robot gripper
box2_pose = geometry_msgs.msg.PoseStamped()
box2_name = "Lego"
grasping_group = "gripper" 
touch_links = robot.get_link_names(group=grasping_group)
box2_pose.pose.position.y = 0.5
box2_pose.pose.position.x = 0.8
scene.attach_box("robotiq_85_left_finger_tip_link" , box2_name, touch_links=touch_links)
"""

"""
# 1b Create an Collision object for PlanningSceneInterface.
print("=== Adding Lego Box to Planning Scene  ===")
# scene = moveit_commander.PlanningSceneInterface()
rospy.sleep(2.0)
box2_pose = geometry_msgs.msg.PoseStamped()
box2_pose.header.frame_id = "robotiq_85_left_finger_tip_link"      # robot.get_planning_frame() 
# box_pose.pose.orientation.w = 1.0
box_pose.pose.position.y = 0.5
box_pose.pose.position.x = 0.8
box2_name = "Lego"
scene.add_box(box2_name, box2_pose, size=(0.04, 0.04, 0.05))
rospy.loginfo(wait_for_state_update(box2_name, scene, box_is_known=True))
"""

# --- 2. Move the TCP above the Red Box
input(" Go to red Box Position => Enter")
joint_goal = group.get_current_joint_values()
joint_goal[0] = np.deg2rad(-64)       # shoulder pan / Basis
joint_goal[1] = np.deg2rad(-72)       # shoulder lift / Schulter
joint_goal[2] = np.deg2rad(93)      # elbow
joint_goal[3] = np.deg2rad(-111)     # wrist1
joint_goal[4] = np.deg2rad(-85)     # wrist2
joint_goal[5] = np.deg2rad(-67)      # wrist3
group.go(joint_goal, wait=True)
print("Reached Goal above plate", joint_goal)


# --- at the end -----
#input("Remove Box")  # Otherwise it will stay
scene.remove_world_object(box_name)
