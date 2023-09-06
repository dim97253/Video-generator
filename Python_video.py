import gpt_request as gpt
import image_generator as imagen
import text_to_speech as tts
import text_to_speech_microsoft as ttsm
from PIL import Image
from moviepy.editor import *

def create_clip(background_image_path, text, voiceover_path):
    # Load the voiceover
    voiceover = AudioFileClip(voiceover_path)    
    # Load the background image and set its duration to match the voiceover
    img = ImageClip(background_image_path).set_duration(voiceover.duration)
    # Generate the text and overlay it on the image
    txt = TextClip(text, fontsize=40, color='white').set_pos('center').set_duration(voiceover.duration)    
    # Combine the text and image
    video = CompositeVideoClip([img, txt])    
    # Add the voiceover to the combined clip
    video = video.set_audio(voiceover)
    return video

def combine_clips(clips):
    return concatenate_videoclips(clips)

print("Enter topic of the video")
topic = input()

video_data = gpt.request_video_slideshow(topic, 6)


# Generate images 
images = []
for data in video_data:
    title = data['title']
    title = title.replace(".", "-")
    img_path = imagen.get_image_local(data['image'])
    # Use Pillow to process the image transparency
    img = Image.open(img_path).convert("RGBA")
    transparent_img = Image.new("RGBA", img.size, (255, 255, 255, 0))
    blended_img = Image.blend(transparent_img, img, alpha=0.5)
    blended_img_path = f'transparent_image_{title}.png'
    blended_img.save(blended_img_path, "PNG")
    images.append(blended_img_path)

# Generate wavs 
wavs = []
for data in video_data:
    # Get voice-over
    wav_name = ttsm.get_wav(data['title'],data['text'])
    wavs.append(wav_name)

# Create clips
clips = []
for i, data in enumerate(video_data):
    # Create clip
    clip = create_clip(images[i], data['title'], wavs[i])
    clips.append(clip)


final_video = combine_clips(clips)
final_video.write_videofile("output.mp4", fps=34)





#print("Enter topic of the video")
#topic = input()

#video_data = gpt.request_video_slideshow(topic, 5)

#for data in video_data:

#    img = imagen.get_image(data['image'])
#    img_path = 'temp.png'
#    with open(img_path, "wb") as f:
#        f.write(img)

#    # Use Pillow to process the image transparency
#    img = Image.open(img_path).convert("RGBA")
#    transparent_img = Image.new("RGBA", img.size, (255, 255, 255, 0))
#    blended_img = Image.blend(transparent_img, img, alpha=0.5)
#    blended_img_path = 'transparent_image.png'
#    blended_img.save(blended_img_path, "PNG")
