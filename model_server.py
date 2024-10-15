import json
import re
from fastapi import FastAPI
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.1", stop=["<|eot_id|>"])

app = FastAPI()

@app.post("/ollama")
async def ollama():
    prompts = await load_prompts(filename="data/prompts.json")
    data = await get_model_response(prompts['system_prompt'], prompts['user_prompt'])
    problems = split_text(data)
    parsed_problems = [parse_problem(problem) for problem in problems if parse_problem(problem).get('question') != "질문 없음"]
    return {"parsed_problems": parsed_problems}

async def get_model_response(user_prompt, system_prompt):
    template = """
        <|begin_of_text|>
        <|start_header_id|>system<|end_header_id|>
        {system_prompt}
        <|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        {user_prompt}
        <|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
        # 단계별로 생각해봅시다.
    """
    prompt = PromptTemplate(input_variables=["system_prompt", "user_prompt"], template=template)
    response = llm.invoke(prompt.format(system_prompt=system_prompt, user_prompt=user_prompt))
    return response

async def load_prompts(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def split_text(text):
    problems = re.split(r"\*\*.*?\*\*", text)
    return [problem.strip() for problem in problems if problem.strip()]

def parse_problem(problem_text):
    question_match = re.search(r"(\d+)\.\s(.*?)(\n\d\))", problem_text)
    question = question_match.group(2) if question_match else "질문 없음"
    explanation_match = re.search(r"# 설명 : (.*)", problem_text)
    explanation = explanation_match.group(1) if explanation_match else "설명 없음"
    options = re.findall(r"\d\)\s(.*?)\n", problem_text)
    answer_match = re.search(r"\* 정답 : (\d)", problem_text)
    answer = answer_match.group(1) if answer_match else None

    return {
        "question": question,
        "options": options,
        "correct_answer": answer,
        "explanation": explanation
    }
