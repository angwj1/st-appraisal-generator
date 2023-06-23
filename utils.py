from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain import LLMChain
from langchain.chains import SequentialChain

import os
import openai

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

def generate_appraisal(api_key, overall_perf_score, strength, achievement, weakness):

	openai.api_key = api_key.strip()

	strength = strength.strip()
	achievement = achievement.strip()
	weakness = weakness.strip()
	overall_perf = get_overall_perf(overall_perf_score)

	llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.7)

	# prompt template 1: rewrite the achievements
	template_string_achievement = """Rewrite the achievements that is delimited by triple backticks, \
	achievement: ```{achievement}``` \
	Use professional tone and easy-to-understand vocabulary. \
	Ouput an empty string i.e. ""  if there is no achievement.
	"""

	first_prompt = ChatPromptTemplate.from_template(template_string_achievement)

	# chain 1: input=achievement and output=achievement_improved
	chain_one = LLMChain(llm=llm, prompt=first_prompt,
	                     output_key="achievement_improved"
	                     )

	# prompt template 2: rewrite the strengths
	if strength != "":
	    template_string_strength = """Rewrite the strengths that is delimited by triple backticks, \
	    strength: ```{strength}``` \
	    Use professional tone and easy-to-understand vocabulary. \
	    """
	else: 
	    template_string_strength = """Output an empty string i.e. ""
	    """

	second_prompt = ChatPromptTemplate.from_template(template_string_strength)

	# chain 2: input=strength and output=strength_improved
	chain_two = LLMChain(llm=llm, prompt=second_prompt,
	                     output_key="strength_improved"
	                     )

	# prompt template 3: rewrite the areas for improvement
	if weakness != "":
	    template_string_weakness = """Rewrite the areas for improvement that is delimited by triple backticks, \
	    areas for improvement: ```{weakness}``` \
	    Use professional tone and easy-to-understand vocabulary. \
	    Ouput an empty string i.e. ""  if there is no areas for improvement.
	    """
	else: 
	    template_string_weakness = """Output an empty string i.e. ""
	    """
	    
	third_prompt = ChatPromptTemplate.from_template(template_string_weakness)

	# chain 3: input=weakness and output=weakness_improved
	chain_three = LLMChain(llm=llm, prompt=third_prompt,
	                       output_key="weakness_improved"
	                       )

	# prompt template 4: final appraisal

	template_string = """Imagine you are a team manager. \
	Write a {overall_perf} performance appraisal in a professional tone. \
	Use the third-person point of view when writing. \
	Do not exceed 120 words. \
	Consider the achievements that is delimited by triple backticks, \
	the strength that is delimited by double hashtags \
	and the areas for improvement that is delimited by double percentages. \
	Ignore input if empty \
	- achievement: ```{achievement_improved}``` \
	- strength: ##{strength_improved}## \
	- areas for improvement: %%{weakness_improved}%% \

	Avoid using complex vocabulary. \
	use [name], [he/she], [him/her] and [his/her] as placeholder
	"""

	fourth_prompt = ChatPromptTemplate.from_template(template_string)
	# chain 4: input= summary, language and output= final appraisal
	chain_four = LLMChain(llm=llm, prompt=fourth_prompt,
	                      output_key="appraisal"
	                      )


	# overall_chain: input=achievement, strength, weakness
	# and output= achievement_improved, strength_improved, weakness_improved, appraisal
	overall_chain = SequentialChain(
	    chains=[chain_one, chain_two, chain_three, chain_four],
	    input_variables=["achievement", "strength", "weakness", "overall_perf"],
	    output_variables=["achievement_improved",
	                      "strength_improved", "weakness_improved", "appraisal"]
	)

	output = overall_chain({'achievement': achievement, 'strength': strength, 'weakness': weakness, 'overall_perf': overall_perf})

	return output["appraisal"]


def generate_chatGPT_prompt(overall_perf_score, strength, achievement, weakness):
	
	strength = strength.strip()
	achievement = achievement.strip()
	weakness = weakness.strip()
	overall_perf = get_overall_perf(overall_perf_score)


	template_string = """Imagine you are a team manager. \
	Write a {overall_perf} performance appraisal in a professional tone. \
	Use the third-person point of view when writing. \
	Do not exceed 120 words. \
	Consider the achievements that is delimited by triple arrobas, \
	the strength that is delimited by double hashtags \
	and the areas for improvement that is delimited by double percentages. \
	Ignore input if empty \
	- achievement: @@@{achievement}@@@ \
	- strength: ##{strength}## \
	- areas for improvement: %%{weakness}%% \

	Avoid the use of complex vocabulary \
	use [name], [he/she], [him/her] and [his/her] as placeholder
	"""

	prompt = template_string.format(overall_perf=overall_perf, strength=strength, achievement=achievement, weakness=weakness)

	return prompt
	

def get_overall_perf(overall_perf_score):
    switcher = {
        1: "very bad and negative",
        2: "negative",
        3: "neutral",
        4: "positive",
        5: "very good and positive",
    }
    return switcher.get(overall_perf_score, "nothing")
