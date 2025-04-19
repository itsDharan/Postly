import json
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from LLM_helper import llm


def process_posts(raw_file_path, processed_file_path=None):
    raw_file_path = os.path.normpath(raw_file_path)  # Ensure correct file path format

    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        enriched_posts = []
        
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = {**post, **metadata}  # Correct dict merging
            enriched_posts.append(post_with_metadata)

    # Unify tags
    unified_tags = get_unified_tags(enriched_posts)
    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}  # Default to original if no mapping found
        post['tags'] = list(new_tags)

    # Handle None case for processed_file_path
    if processed_file_path:
        processed_file_path = os.path.normpath(processed_file_path)
        with open(processed_file_path, mode="w", encoding="utf-8") as outfile:
            json.dump(enriched_posts, outfile, indent=4)


def extract_metadata(post):
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post, and tags.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, language, and tags. 
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means Hindi + English).
    
    Here is the actual post on which you need to perform this task:  
    {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke({"post": post})  # Fixed input format

    try:
        json_parser = JsonOutputParser()
        metadata = json_parser.parse(response.content)  # Ensure valid JSON parsing
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse metadata.")

    return metadata


def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])

    unique_tags_list = ','.join(unique_tags)

    template = '''I will give you a list of tags. You need to unify tags with the following requirements:
    1. Tags should be merged into a shorter list when possible. 
       Example: "Jobseekers" and "Job Hunting" → "Job Search"
    2. Tags must follow title case (e.g., "Motivation", "Job Search").
    3. Return a JSON object with original tags mapped to unified tags.
       Example: {{"Jobseekers": "Job Search", "Job Hunting": "Job Search"}}
    
    Here is the list of tags: 
    {tags}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke({"tags": unique_tags_list})

    try:
        json_parser = JsonOutputParser()
        unified_tag_mapping = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse tag mapping.")

    return unified_tag_mapping


if __name__ == "__main__":
    process_posts("Data/raw_post.json", "processed_posts.json")  # Fixed output file name
