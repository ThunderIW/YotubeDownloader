from pytube import YouTube,Playlist
from moviepy.editor import VideoFileClip, AudioFileClip
import dearpygui.dearpygui as dpg
import urllib.request
from PIL import Image
from test import sort_reslution



import os

res_set=set()






def Download_thumbnailImage_set_info(sender,app_data):

    global res_set

    YT = YouTube(dpg.get_value("-Link-"))
    Video_title=YT.title
    Author=YT.author
    thumbnailImage=YT.thumbnail_url
    urllib.request.urlretrieve(thumbnailImage,fr"D:\UBCO\COSC_301_labs\In_class_examples\GIS\thumbnail\t.png")

    for res in YT.streams.filter(file_extension="mp4"):
        res_set.add(res.resolution)

    t=list(res_set)
    t.remove(None)
    available_resolution=sort_reslution(t)







    image = Image.open(fr"D:\UBCO\COSC_301_labs\In_class_examples\GIS\thumbnail\t.png")
    image.thumbnail((400,200))
    image.save(fr"D:\UBCO\COSC_301_labs\In_class_examples\GIS\thumbnail\t.png")


    width, height, channels, data = dpg.load_image(fr"D:\UBCO\COSC_301_labs\In_class_examples\GIS\thumbnail\t.png")

    tag_Format=f"{Video_title}"

    with dpg.texture_registry():
        dpg.add_static_texture(width=width, height=height, default_value=data, tag=tag_Format)



        dpg.configure_item("-VT-",texture_tag=tag_Format,show=True)
        dpg.configure_item("-RT-",show=True)



    dpg.set_value("-title-",Video_title)
    dpg.set_value("-Author-",Author)
    dpg.configure_item("-R-", items=available_resolution, show=True)
    dpg.set_viewport_height(700)


def get_video(sender,app_data):
    global tag
    YT = YouTube(dpg.get_value("-Link-"))
    res_choice=dpg.get_value("-R-")
    print(res_choice)

    for i in YT.streams.filter(file_extension="mp4",progressive=False,resolution=res_choice):
        print(i)
        if i.resolution==res_choice:
            tag=i.itag

    YT.streams.get_by_itag(tag).download(output_path="downloadedFile",filename="Video.mp4")
    YT.streams.get_audio_only().download(filename="music.mp3",output_path="downloadedFile")



    video_path=r"D:\UBCO\COSC_301_labs\In_class_examples\GIS\downloadedFile\Video.mp4"
    audio_path=r"D:\UBCO\COSC_301_labs\In_class_examples\GIS\downloadedFile\music.mp3"

    video_clip=VideoFileClip(video_path)
    audio_clip=AudioFileClip(audio_path)

    video_clip=video_clip.set_audio(audio_clip)

    video_clip.write_videofile(r"D:\UBCO\COSC_301_labs\In_class_examples\GIS\outputVideo\f.mp4", codec='libx264',
                               audio_codec='aac')

    output_file=f"{YT.title}_{YT.author}"

    os.rename(r"D:\UBCO\COSC_301_labs\In_class_examples\GIS\outputVideo\f.mp4",fr"D:\UBCO\COSC_301_labs\In_class_examples\GIS\outputVideo\{output_file}.mp4")
    os.remove(r"D:\UBCO\COSC_301_labs\In_class_examples\GIS\downloadedFile\music.mp3")
    os.remove(r"D:\UBCO\COSC_301_labs\In_class_examples\GIS\downloadedFile\video.mp4")






dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=300)
width, height, channels, data = dpg.load_image("Sample-PNG-Free-Image.png")
with dpg.texture_registry(show=False):
    dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")




with dpg.window(label="Example Window",tag="T"):

    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Settings")
            dpg.add_menu_item(label="Exit")


        with dpg.menu(label="Settings"):
            with dpg.group(horizontal=True):
                dpg.add_text("Output video Location")
                dpg.add_input_text(tag="-OuputLoc-")
            dpg.add_button(label="SET")


    with dpg.tab_bar():
        with dpg.tab(label="Main"):
            dpg.add_image("texture_tag",show=False,tag="-VT-")
            with dpg.group(label="VIDEO_Link",horizontal=True):
                dpg.add_text("Video link")
                dpg.add_input_text(hint="Enter the youtube link here",tag="-Link-",callback=Download_thumbnailImage_set_info)





            with dpg.group(label="VIDEO_TITLE",horizontal=True):
                dpg.add_text("Video Title")
                dpg.add_input_text(tag="-title-")

            with dpg.group(label="VIDEO_AUTHOR",horizontal=True):
                dpg.add_text("Video Author")
                dpg.add_input_text(tag="-Author-")

            dpg.add_text("Resolution",show=False,tag="-RT-")
            dpg.add_radio_button(tag="-R-",items=[],show=False,horizontal=True,default_value="1080p")



            dpg.add_button(label="Download Video",callback=get_video)










dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("T",True)
dpg.start_dearpygui()
dpg.destroy_context()












