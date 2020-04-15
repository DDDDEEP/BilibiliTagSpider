import request from 'umi-request';
import { TableListParams, VideoTableListParams } from './data.d';

export async function getVideoTagList(params?: TableListParams) {
  return request('/api/video_tag', {
    params,
    method: 'GET',
  });
}

export async function getVideoListByTag(params?: VideoTableListParams) {
  return request('/api/video/by_tag', {
    params,
    method: 'GET',
  });
}
