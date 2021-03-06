import {axiosInstance as axios} from './index';

const DOCUMENT_API = window.documentApi || '/api/v1/document/';

export default {
  updateDocument(document) {
    return axios.put(DOCUMENT_API, document);
  },
  createDocument(document) {
    return axios.post(DOCUMENT_API, document);
  },
  removeDocument(documentId) {
    return axios.delete(`${DOCUMENT_API}${documentId}/`);
  },
}
