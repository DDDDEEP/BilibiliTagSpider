import request from 'umi-request';
import { TableListParams } from './data.d';

export async function getTagAvgStattList(params?: TableListParams) {
  return request('/api/rank/tag_avg_stat', {
    params,
    method: 'GET',
  });
}
