import request from 'umi-request';
import { TableListParams } from './data.d';

export async function getTagCountList(params?: TableListParams) {
  return request('/api/rank/tag_count', {
    params,
    method: 'GET',
  });
}
