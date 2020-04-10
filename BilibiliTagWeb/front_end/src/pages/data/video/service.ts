import request from 'umi-request';
import { TableListParams } from './data.d';

export async function getVideoList(params?: TableListParams) {
  return request('/api/video', {
    params,
    method: 'GET',
  });
}

