import { defineStore } from 'pinia';
import videoapi from '../stores/apiVideo';

export const useVideoSerialsStore = defineStore('videoSerials', {
  state: () => {
    return {
      is_loading: false,
      videoSerialName: '最伟大的作品',
      videos: [],
      coverImg: 1
    };
  },
  actions: {
    async upload_videos() {
      try {
        // 让btn处于loading状态
        this.is_loading = true;

		// 循环包裹并上传videos列表中的每个视频
        // 若只有一个则不需要for循环
        for (const item of this.videos) {
          // 针对后端接口，二进制文件及其他参数均需包裹进FormData对象中
          const videoData = new FormData();
          // 添加二进制文件方法
          videoData.append('videoFile', item);
          // 添加非字符串数据：此处数字为外键字段
          videoData.append(
            'coverImg',
            JSON.stringify(this.coverImg)
          );
          // 添加字符串数据
          videoData.append('videoSerialName', this.videoSerialName);

          // 数据包装完成，上传
          await videoapi.post_video(videoData);
        }

		// 上传完毕，让btn解除loading状态
        this.is_loading = false;

      } catch (error) {
        this.is_loading = false;
        console.log(error);
      }
    },
  },
});
