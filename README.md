**An English version of this software tool is planned for release in the near future. Please stay tuned!**

小米坡word文档转视频生成工具，是一款基于windows平台下使用的word文档转视频工具。可以把word文档的图片转成视频、提取文档里边的文字转成配音、并生成字幕同步在视频上展示，支持加背景音乐。最终形成一个有配音、画面、字幕、背景音乐的完整视频。

软件免费使用，软件暂时不能完全离线，因为集成了python的edge-tts模块，因edge-tts需要联网，所以软件需要联网才能使用。

但软件支持集成任何自建tts服务或其它tts，如果用户自建了tts，则完全离线没问题了。

v1.13b起，增加一个新版本检查，如软件发现有新版本，会在界面上提示用户。

除此之外，无其它网络请求。


**软件下载**

软件无注册无登录，绿色解压直接免费使用。
如遇到使用问题或需要更多了解，可查看软件官网
https://word2video.xiaomipo.com/

**使用教程视频**
https://www.bilibili.com/video/BV1TouDeTEPL/

**视频演示**

基本视频演示，主要演示软件功能和技术效果，可能视频不好看不好听（这和配图、选歌、故事情节字幕有关系）。

视频演示链接 https://www.bilibili.com/video/BV1UjuDerEok/ 查看生成演示视频所用word文档

如果你有优秀的作品当案例，可以联系发链接给作者。

**软件使用**

v1.15b完成更多功能的迭代，已经进行了大量的新功能与布局，以下使用教程仅供欣赏，更多请见上文视频教程或官网。

![image](https://github.com/feng8088/word2video/blob/main/1.15b-demo.gif)

虽然看起来操作选项很多，但都是可选操作。 生成视频的操作默认只需要4步即可。

（1）素材设置界面下，选一个word文档
（2）素材设置界面下，选一个背景音乐
（3）素材设置界面下，设置一下视频保存目录
（4）生成视频界面下，点击 开始生成


**使用教程**

软件绿色安装，下载压缩包后解压，运行 word2video.exe 打开软件

先准备一个小故事，内容不限。然后给故事配图，可以用AI生成，也可以自己找素材。

演示案例中，作者给大家演示一个用word做一个关于成语”亡羊补牢“的有声视频

（1）准备word文档（一行文字一个图片或一个图片一行文字），文字不能比图片少

word2video word文档转视频 文档素材格式

（2）准备一首背景音乐MP3，

word2video word文档转视频 音频素材格式

（3）解压缩软件，运行 word2video.exe，进行word文档转视频。（所有的参数都要选）

word2video word文档转视频 软件运行界面

软件生成视频期间会闪动并快速秒自动弹出关闭新窗口，这是因为软件依赖会调用出CMD控制台，属于正常情况。作者也在努力隐藏这个控制台，还在努力中。

![image](https://github.com/feng8088/word2video/blob/main/22222.png)

（4）软件的文字转语音使用了python的edge-tts模块，因edge-tts需要联网，所以软件需要联网才能使用。

word2video word文档转视频 软件输出MP4界面

**注意：**

根据硬件CPU的性能，在word转视频 与 音频合并到视频 这两个步骤，耗时会比较长，而且看不到状态进度，需要耐心等。

可在导出目录看已经生成的文件，最终在导出列表中有许多文件，用户可以保留或删除。

word2video word文档转视频 输出文件列表

![image](https://github.com/feng8088/word2video/blob/main/33333.png)

