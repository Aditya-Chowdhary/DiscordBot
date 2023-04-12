# from discord import FFmpegPCMAudio
# import youtube_dl

# def download_audio(yt_url):
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#         }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([yt_url])

# yt_url = 'https://www.youtube.com/watch?v=8OAPLk20epo'
# download_audio(yt_url)

# import youtube_dl

# ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

# with ydl:
#     result = ydl.extract_info(
#         'https://www.youtube.com/watch?v=8M6PhD0v9TE',
#         download=False # We just want to extract the info
#     )

# if 'entries' in result:
#     # Can be a playlist or a list of videos
#     video = result['entries'][0]
# else:
#     # Just a video
#     video = result

# print(video)
# video_url = video['url']
# print(video_url)

# from youtube_dl import YoutubeDL
# audio_downloader = YoutubeDL({'format':'bestaudio'})
# try:
#     print('Youtube Downloader'.center(40, '_'))
#     URL = 'https://www.youtube.com/watch?v=8M6PhD0v9TE'
#     audio_downloader.extract_info(URL)
# except Exception:
#     print("Couldn\'t download the audio")


from pytube import YouTube

link = 'https://www.youtube.com/watch?v=8M6PhD0v9TE'
yt = YouTube(link)

downloader = yt.streams.filter(only_audio=True).get_audio_only()
downloader.download()
title = yt.title
for i in "!@#$%^&*\(\)\{\}|":
    title = title.replace(i, '')
print(title+'.mp4')