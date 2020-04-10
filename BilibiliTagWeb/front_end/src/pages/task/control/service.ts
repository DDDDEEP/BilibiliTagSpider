import request from 'umi-request';
import { TableListParams, TaskStartParams, RecordListParams } from './data.d';

export async function getTaskList(params?: TableListParams) {
  return request('/api/task/task_list', {
    params,
    method: 'GET',
  });
}

export async function startSpider(params?: TaskStartParams) {
  return request('/api/task/start_spider', {
    data: params,
    method: 'POST',
    requestType: 'form',
  });
}

export async function startHandler(params?: TaskStartParams) {
  return request('/api/task/start_handler', {
    data: params,
    method: 'POST',
    requestType: 'form',
  });
}

export async function getReocrdList(params?: RecordListParams) {
  return request('/api/record', {
    params,
    method: 'GET',
  });
}
