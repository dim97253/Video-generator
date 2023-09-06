from http.client import responses
import os
import openai
import json
import re


openai.api_key = ""

def extract_text(s):
    pattern = r'```(.*?)```'
    matches = re.findall(pattern, s, re.DOTALL)    
    #cleaned_matches = [match.replace("\\n", "").replace("\n", "") for match in matches]    
    return matches[0]

def request_presentation(topic, size):

    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
        {
          "role": "system",
          "content": f"Generate {size} slides presentation. Format the response in JSON. Json should contain array of slides.\nEach item in array should contain:\n- string \"title\" of the slide.\n- string \"text\" for main text.  \n- string \"image\" for artists to draw an image or photo. it should describe what is expected to be on image. The artist is an AI, so don't ask anything complex.\n- (optional) object \"chart\" that contains string \"title\", number array \"datapoints\" and names of axis. \"xname\" and \"yname\" for building a linechart. (no more than 10 datapoints). Only if text assumes any charts. \nPut entire JSON result between ``` symbols"
        },
        {
          "role": "user",
          "content": f"Presentation topic is \"{topic}\""
        }
      ],
      temperature=1,
      max_tokens=1996,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    json_string = response.choices[0].message.content

    #json_string = """```
    #[
    #  {
    #    "title": "Introduction to Generative AI",
    #    "text": "Generative AI is one of the biggest recent advancements in artificial intelligence technology due to its ability to create. It works by developing new pieces of content from scratch, such as texts, images, and videos. This type of AI holds tremendous promise as it offers a way to harness the creativity of machines to assist in several domains.",
    #    "image": "Illustration of a robot hand holding a pencil and sketching on paper. The paper shows a mix of text, images and diagrams, indicating content creation by the AI."
    #  },
    #  {
    #    "title": "Evolution of Generative Models Over the years",
    #    "text": "In the last five years, there's been a rapid increase in the size of generative models. Each year, the models are growing larger, empowering them to generate more intricate and realistic content. This suggests that the field of generative AI is rapidly improving.",
    #    "image": "A line chart showing an uphill line, indicating the increase in model sizes over the years",
    #    "chart": {
    #      "title": "Average Generative Model Sizes Over The Last Five Years",
    #      "datapoints": [100, 200, 500, 900, 1500],
    #      "xname": "Year",
    #      "yname": "Model Size (in Billion Parameters)"
    #    }
    #  }
    #]```"""

    json_string = extract_text(json_string)
    
    data_array = json.loads(json_string)
    return data_array

def request_video_slideshow(topic, size):
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
        {
          "role": "system",
          "content": f"Generate {size} slides for slide-show video. Format the response in JSON. Json should contain array of slides.\nEach item in array should contain:\n- string \"title\" of the slide.\n- string \"text\" for main text.  \n- string \"image\" for artists to draw an image or photo. it should describe what is expected to be on image. The artist is an AI, so don't ask anything complex. \nPut entire JSON result between ``` symbols. \nTemplate:```[{...},{...}....]```"
        },
        {
          "role": "user",
          "content": f"Slide-show video topic is \"{topic}\""
        }
      ],
      temperature=1,
      max_tokens=2000,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    json_string = response.choices[0].message.content
    json_string = extract_text(json_string)    
    data_array = json.loads(json_string)
    return data_array

