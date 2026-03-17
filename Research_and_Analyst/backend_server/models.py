import operator 
from typing import List, Annotated
from langgraph.graph import MessagesState
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

#--------------------------------------
# Section Model 
#--------------------------------------
class Section(BaseModel):
    title: str
    content: str

#--------------------------------------
# Analyst Models
#--------------------------------------
class Analyst(BaseModel):
    affiliation: str = Field(description="Primary Affiliation of the analyst")
    name: str = Field(description = "Name of the analyst")
    role: str = Field(description ="Role of the analyst in the context of the topic")
    description: str = Field(description = "Description of the analyst's focus, concerns, and motives")

    @property
    def persona(self)-> str:
        return(
            f"Name: {self.name}\n"
            f"Role: {self.role}\n"
            f"Affiliation: {self.affiliation}\n"
            f"Description: {self.description}\n"
        )

# This class will contain a list of analysts 
class Perspective(BaseModel):
    analysts: List[Analyst] = Field(description = "Comprensive list of analysts with their roles, affiliations. ")

#--------------------------------------
# Search Query Output Parser
#--------------------------------------
class SearchQuery(BaseModel):
    search_query: str = Field(description="Search query for retrieval")


#--------------------------------------
# State Classes for Graph
#--------------------------------------
# This is for 1st Workflow
class GenerateAnalystsState(TypedDict):
    topic: str # Number of analysts to generate
    max_analysts: int # Number of analysts to generate
    human_analyst_feedback: str # Feedback from human 
    analysts: List[Analyst] # List of analysts generated

# This is for 2nd Workflow
class InterviewState(MessagesState):
    max_num_turns: int # Maximum interview turns allowed
    context: Annotated[str, operator.add] # Retrieved or searched context
    analyst: Analyst # Analyst conducting interview
    interview: str # Full interview transcript
    sections: list # Generated section from interview

# This is for 3rd Workflow
class ResearchGraphState(TypedDict):
    topic: str # Research topic
    max_analysts: int # Number of analysts 
    human_analyst_feedback: str # Optional feedback from human
    analysts: List[Analyst] # All analysts involved
    sections: List[Analyst] # All analysts involved
    sections: Annotated[list, operator.add] # All interview-generated sections
    introduction: str # Introduction of final report 
    content: str # Main content of report
    conclusion: str # Conclusion of final report
    final_report: str # Complied report string