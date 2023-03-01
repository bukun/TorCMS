import { file } from "../api";

const fileService = {
  upload: async function (fileObj, progressCallback) {
    return file.upload(fileObj, progressCallback).then((res) => {
      console.log(res);
      return res.data;
    })
  },
  bigUpload: async function (fileObj, progressCallback) {
    return file.bigUpload(fileObj, progressCallback).then((res) => {
      console.log(res);
      return res.data;
    })
  }
};

export { fileService };
