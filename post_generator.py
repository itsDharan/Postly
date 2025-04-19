# post_generator.py
# post_generator.py
from LLM_helper import llm
from few_shot import FewShotPosts

def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"

def get_prompt(length, language, tag, dataset_name):
    length_str = get_length_str(length)
    prompt = f'''
    Generate a LinkedIn post in the style of {dataset_name.split('_')[0]} using the below information. No preamble.
    1) Topic: {tag}
    2) Length: {length} ({length_str})
    3) Language: {language}
    
    Special Instructions:
    - If Language is Hinglish: Use a mix of Hindi and English
    - For other languages: Write entirely in that language
    - Maintain professional tone
    - Include relevant hashtags
    - Match the writing style of {dataset_name.split('_')[0]}
    '''

    few_shot = FewShotPosts(dataset_name)
    examples = few_shot.get_filtered_posts(length, language, tag)
    
    if len(examples) > 0:
        prompt += "\n\nExamples of similar posts:\n"
        for i, post in enumerate(examples[:3]):  # Show max 3 examples
            prompt += f"\nExample {i+1}:\n{post['text']}\n"

    return prompt

def generate_post(length, language, tag, dataset_name):
    prompt = get_prompt(length, language, tag, dataset_name)
    response = llm.invoke(prompt)
    return response.content