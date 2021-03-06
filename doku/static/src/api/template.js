import {axiosInstance as axios} from './index';

const TEMPLATE_API = window.templateApi || '/api/v1/template/';

export default {
  updateTemplate(template) {
    return axios.put(TEMPLATE_API, template);
  },
  fetchTemplates(options) {
    options = options || {};
    return axios.get(TEMPLATE_API, options);
  },
  addStylesheet(url, stylesheet) {
    return axios.post(url, stylesheet);
  },
  removeStylesheet(url, stylesheet) {
    // Note: axios.delete does not support a request body. It accepts
    // two parameters: url and optional config.
    return axios.delete(url, {data: stylesheet});
  }
}
