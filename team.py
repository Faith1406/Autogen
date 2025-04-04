import asyncio
#this is the model factory 
from model_factory import get_model_client as gt 
#other team chats imports
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken

class Team:
    def __init__(self,provider_1, provider_2, model_1, model_2, system_message_1, system_message_2, description_1, description_2, termination_text="Approve", api_key_1=None, api_key_2=None, behaviour_1="primary", behaviour_2="critic",):

        self.model_1 = model_1
        self.model_2 = model_2
        self.provider_1 = provider_1
        self.provider_2 = provider_2
        self.termination_text = termination_text
        self.api_key_1 = api_key_1
        self.api_key_2 = api_key_2
        self.behaviour_1 = behaviour_1 
        self.behaviour_2 = behaviour_2
        self.description_1 = description_1
        self.description_2 = description_2 
        self.system_message_1= system_message_1 
        self.system_message_2= system_message_2 
        
        self.primary_model = gt(
            provider = self.provider_1,
            model_name = self.model_1,
            api_key = self.api_key_1,
        )
        self.secondary_model = gt(
            provider = self.provider_2,
            model_name = self.model_2,
            api_key = self.api_key_2,
        )
        self.primary_agent = AssistantAgent(
            self.behaviour_1,
            model_client = self.primary_model,
            description = self.description_1,
            system_message = self.system_message_1,
        )
        self.critic_agent = AssistantAgent(
            self.behaviour_2,
            model_client = self.secondary_model,
            description = self.description_2,
            system_message = self.system_message_2, 
        )
        self.text_termination = TextMentionTermination(self.termination_text)
        self.team = RoundRobinGroupChat([self.primary_agent, self.critic_agent], termination_condition = self.text_termination)


    async def print_convo(self, text_input:str):
        await Console(self.team.run_stream(task=text_input))

    def run_team(self, text_input:str):
        asyncio.run(self.print_convo(text_input))

    def display_team_members(self):
        print(f"You created the team of {self.model_1, self.model_2}")

