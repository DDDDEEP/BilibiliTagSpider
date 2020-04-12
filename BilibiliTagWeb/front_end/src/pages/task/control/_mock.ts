// eslint-disable-next-line import/no-extraneous-dependencies
import moment from 'moment';
import { Request, Response } from 'express';
import { parse } from 'url';
import { TaskTableListItem, TableListParams, RecordListItem, RecordListParams } from './data.d';
// import { monthFixZero } from '@/utils/utils';

const monthFixZero = (month: number) => {
  return month.toString().padStart(2, '0');
}

// mock tableListDataSource
let tableListDataSource: TaskTableListItem[] = [];

for (let i = 0; i < 8; i += 1) {
  const randomTimeStart: number = Math.round(Math.random() * 10000000000);
  const progressCur: number = Math.round(Math.random() * 1000000);
  tableListDataSource.push({
    task_id: Math.random().toString(36).substr(2),
    task_type: i % 2,
    tid: 17,
    time_from: 20150101,
    time_to: 20161231,
    time_start: randomTimeStart,
    time_end: (i % 2 ? -1 : randomTimeStart + 10000000),
    state: ['PENDING', 'STARTED', 'PROGRESS', 'SUCCESS', 'ERROR'][i % 5] as
      | 'PENDING' 
      | 'STARTED' 
      | 'PROGRESS' 
      | 'SUCCESS'
      | 'ERROR',
    progress: i % 2 ? [
      {
        cur: progressCur,
        total: progressCur + 100000,
      },
      {
        cur: progressCur,
        total: progressCur + 100000,
      },
    ] : [
      {
        cur: progressCur,
        total: progressCur + 100000,
      },
    ],
    extra: i % 2 ? {} : { status: Math.round(Math.random() * 100) % 5 },
  });
}

function getTaskList(req: Request, res: Response, u: string) {
  let dataSource = tableListDataSource;

  let url = u;
  if (!url || Object.prototype.toString.call(url) !== '[object String]') {
    // eslint-disable-next-line prefer-destructuring
    url = req.url;
  }

  const params = (parse(url, true).query as unknown) as TableListParams;

  params.pageIndex = parseInt(params.pageIndex);
  params.pageSize = parseInt(params.pageSize);
  const startIndex:number = (params.pageIndex - 1) * params.pageSize
  const endIndex:number = startIndex + params.pageSize
  const result = {
    status: 0,
    data: {
      results: dataSource.slice(startIndex, endIndex),
      count: dataSource.length,
    },
    errors: [],
    message: 'success'
  };

  return res.json(result);
}

function startSpider(req: Request, res: Response, u: string, b: Request) {
  const result = {
    status: 0,
    data: {
    },
    errors: [],
    message: 'success'
  };

  return res.json(result);
}

function startHandler(req: Request, res: Response, u: string, b: Request) {
  const result = {
    status: 0,
    data: {
    },
    errors: [],
    message: 'success'
  };

  return res.json(result);
}

function getRecordList(req: Request, res: Response, u: string) {
  let url = u;
  if (!url || Object.prototype.toString.call(url) !== '[object String]') {
    // eslint-disable-next-line prefer-destructuring
    url = req.url;
  }

  const params = (parse(url, true).query as unknown) as RecordListParams;

  let dataSource: RecordListItem[] = [];
  const year = moment(params.pubdate_min * 1000).year();
  for (let monthIndex = 1; monthIndex < 6; ++monthIndex) {
    for (let dayIndex = 7; dayIndex < 20; ++dayIndex) {
      dataSource.push({
        tid: params.tid,
        pubdate: Math.floor(moment(`${year}-${monthFixZero(monthIndex)}-${monthFixZero(dayIndex)}`).valueOf() / 1000),
        status: dayIndex % 3,
      })
    }
  }

  const result = {
    status: 0,
    data: {
      results: dataSource,
      count: dataSource.length,
    },
    errors: [],
    message: 'success'
  };

  return res.json(result);
}

export default {
  'GET /api/task/task_list': getTaskList,
  'POST /api/task/start_spider': startSpider,
  'POST /api/task/start_handler': startHandler,
  'GET /api/record': getRecordList,
};
