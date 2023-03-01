import { api } from 'boot/axios';

const HEADERS = {
  'Content-Type': 'application/x-www-form-urlencoded'
};

const file = {
  upload: async function(data, progressCallback) {
    console.log('file->upload')
    return api.post('/entity_j/quasar_add' , data,
      {
        headers: HEADERS,
        onUploadProgress:  (progressEvent) => {
          if (progressCallback) {
            progressCallback(progressEvent)
          }
        }
    });
  },
  bigUpload: async function(data, progressCallback) {
    console.log('file->bigUpload')
    return api.post('/api/file/big' , data,
      {
        headers: HEADERS,
        onUploadProgress:  (progressEvent) => {
          if (progressCallback) {
            progressCallback(progressEvent)
          }
        }
    });
  }
};

export { file };
