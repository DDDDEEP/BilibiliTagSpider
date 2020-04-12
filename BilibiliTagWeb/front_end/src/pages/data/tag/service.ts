import request from 'umi-request';
import { TableListParams } from './data.d';

export async function getTagList(params?: TableListParams) {
  return request('/api/tag', {
    params,
    method: 'GET',
  });
}

