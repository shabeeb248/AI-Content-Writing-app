prompt_1="""
Given the following main keyword and supporting keywords, generate 5 creative and catchy article title suggestions. 
The titles should incorporate best practices for engaging and traffic-driving headlines, including the use of numbers, clarity, direct address to the reader, and emotional or power words. 
The main keyword should be prominently featured in all titles, and at least half of the suggestions should include a number at the beginning. 
Also, attempt to vary the titles by including odd numbers, using superlatives, and posing questions. 
Reflect on incorporating the principles shared by Brandon Gaille, ensuring the titles are concise, clear, and tailored to potentially improve Google rankings and social shares.
Please provide the title alone in the Output Format, without any numerical or alphabetical or bullet listing before the title.

Main Keyword :{}

Supporting Keywords:{}

The output response should be a list of titles, formatted as follows, without any additional text before or after it:

Output format:
["title_1", "title_2", ...]


Output:

"""
prompt_subtitle="""
Given the following title of a blog, generate 5 subsection titles (subtitles). The output subtitles should be in the given Output Format.
Please provide the title alone in the Output Format, without any numerical or alphabetical or bullet listing before the title.

Blog title :{}

The output response should be a list of 5 subtitles, formatted as below Output Format, without any additional text before or after it:

Output Format:
["subtitle_1", "subtitle_2", "subtitle_3","subtitle_4","subtitle_5"]


Output:

"""

prompt_content="""
You are article writer, you need to write arricle from given Main Title and also Subtitle, just craete the article content only from the given Subtitle by understnng the overall article structure from it.
Main Title:{}
Subtitle :{}

Content Generated till now : 
{}

The output response should be a content for the above Subtitle, without any additional text before or after it:

Output:
"""

prompt_image="""
Create an engaging and thematic image for a blog title The image should visually represent the core theme of the blog, incorporating relevant elements and symbols that align with the subject matter. 
Aim for a style that captures the essence of the topic, making it suitable for use as a blog header or featured image. 
Ensure the composition is balanced and the imagery is clear and compelling. 

Blog title :{}



The output response should be a image, without any additional text before or after it:

Output:

"""
