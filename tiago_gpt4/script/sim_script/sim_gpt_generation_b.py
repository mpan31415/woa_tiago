#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import openai
from sim_text_to_speech_gpt4 import TTSFunction
import yaml
import os
from sim_create_calendar import create_event_calendar
from sim_Showing_Events_Caleder import Showing_Events_Calender
from sim_breathing import BreathingExercise
from sim_handover_snacks import GetSnack
from sim_strech_ball import CatchBall
from sim_def_actions import play_action
from sim_customized_gesture import FollowMe, ShowAround


# Configure your OpenAI API key here
current_dir = os.path.dirname(__file__)  # Gets the directory of the current script
config_path = os.path.join(current_dir, '..', '..', 'config', 'gpt_api.yaml')  # Navigate to the config.yaml file
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)
openai.api_key = config['api_key']

class GenerationFuncion():
    def __init__(self):
        self.speak = TTSFunction()
        self.follow_me = FollowMe()
        self.show_around = ShowAround()

    def process_with_gpt4(self, text):
        try:
            rospy.loginfo("Start generate by gpt")
            keyword_list= ['no_action', 'stress_ball', 'breathing_exercise', 'provide_snack', 'schedule_meeting', 'navigate_to_meeting_room_A', 'navigate_to_meeting_room_B', 'navigate_to_kitchen', 'say_hi_wave_hand']
            gpt_response = openai.chat.completions.create(
                model="gpt-4",  # Use the model identifier for GPT-4. Adjust if you're using a specific variant.
                messages=[{"role": "system", "content": 
                           "You are a helpful office assistant robot. Your name is Tiago and you are Australian. You can assist office work and maintain a relax vibe. \
                           Now you are tested in a robot competion fo a human-robot conference. \
                           Info on Human-Robot-Interaction conference: 19th Annual ACM/IEEE International Conference on Human Robot Interaction (HRI). HRI 2024 is the 19th annual conference for basic and applied HRI research. Researchers from across the world present their best work to HRI to exchange ideas about the theory, technology, data, and science furthering the state-of-the-art in the field. The conference theme for HRI 2024 is 'HRI in the real world' and will focus on key HRI theories, designs, studies, systems, and technical advances that aim to bring HRI out of the lab and into everyday life. We encourage the community to consider what it means to do HRI in practice, and ways to bring it into the mainstream. The HRI 2024 conference is taking place in Boulder, Colorado, in the US.\
                           Info on the robot competition: The interaction is taking place during the HRI 2024 Robot Competition. It is the first competition at the HRI conference and the task is to develop human-robot applications designed to provide invaluable assistance and companionship to workers in the office environment. The competition serves as a platform for participants to demonstrate the capabilities of their robots and to highlight the ways in which these intelligent machines can enhance the productivity and well-being of office professionals. Participants are invited to present their human-robot applications based on the Tiago Platform, each with its unique add-ons design, features, and functionalities. These robots should behave as humanly as possible, fostering a sense of familiarity and promoting natural interaction with humans. They should understand human emotions, displaying expressive facial features and gestures that enable effective communication and empathetic engagement.The person the robot is interacting with during the competition is from a jury. The jury will score the interaction. For instance: The robot’s Conversational Ability, i.e. How well does the robot engage in conversations with users? Does it understand and respond appropriately to user queries and requests? Is the conversation natural and fluid? Besides, the robot has to convey emotional intelligence, i.e. How well does the robot understand and respond to human emotions? Does it display empathy and provide emotional support when needed?\
                           "
                           }, 
                          {"role": "user", "content": 
                           f"{text}. \
                           Note: Please response with proper natural language and provide a keyword after a * sign, without a period mark. \
                           The keyword should be choose from this list: [{keyword_list}]\
                            For example: Sure, come with me. *navigate_to_meeting_room_a\
                           "}],
            )
            rospy.loginfo("GPT responsed")
        

            gpt_response = gpt_response.choices[0].message.content
            rospy.loginfo("GPT responsed")
            robot_response, action_keyword = gpt_response.split("*")
            rospy.loginfo(f"Robot response is: {robot_response}")
            rospy.loginfo(f"Action is: {action_keyword}")
            self.speak.text_to_speech(robot_response, 1.0)
            if action_keyword != "no_action":
                if action_keyword == "breathing_exercise":
                    rospy.loginfo("Doing Breathing Exercises")
                    breathing = BreathingExercise()
                    breathing.run()
                elif action_keyword == "provide_snack":
                    rospy.loginfo("Doing Get a Snack")
                    snake = GetSnack()
                    snake.run()
                elif action_keyword == "stress_ball":
                    rospy.loginfo("Doing Stress Ball")
                    ball = CatchBall()
                    ball.run()
                elif action_keyword == "say_hi_wave_hand":
                    rospy.loginfo("Doing a wave")
                    play_action('wave')
                    play_action('home')
                elif action_keyword == "schedule_meeting":
                    rospy.loginfo("Doing schedule a meeting")
                    # todo: turn around
                    create_event_calendar()
                    # todo: turn around
                    schedule = Showing_Events_Calender()
                    rospy.loginfo(schedule)
                    self.speak.text_to_speech(schedule, 1.2)
                elif action_keyword == "navigate_to_meeting_room_A":
                    rospy.loginfo("Show meeting room A")
                    self.follow_me.run()

                    text = "This is the meeting room B. You can have a meeting here."
                    self.show_around.run(text)

                elif action_keyword == "navigate_to_meeting_room_B":
                    rospy.loginfo("Show meeting room B")

                    text = "This is the meeting room B. You can have a meeting here."
                    self.show_around.run(text)

                elif action_keyword == "navigate_to_kitchen":
                    rospy.loginfo("Show kitchen")
                    self.follow_me.run()
                    
                    text = "This is the kitchen. Help yourself to a cup of coffee."
                    self.show_around.run(text)
                else:
                    rospy.loginfo("Wrong keyword.")

            return robot_response
        except Exception as e:
            rospy.logerr(f"Failed to process text with GPT-4: {e}")
            return "Error processing text with GPT-4."