// eslint-disable-next-line import/no-extraneous-dependencies
import moment from 'moment';
import { Request, Response } from 'express';
import { parse } from 'url';
import { TableListParams, TagTableListItem } from './data.d';

// mock tableListDataSource
let tableListDataSource: TagTableListItem[] = [];

for (let i = 0; i < 200; i += 1) {
  tableListDataSource.push({
    title: Math.random().toString(36).substr(2)
  });
}

function getTagList(req: Request, res: Response, u: string) {
  let dataSource = tableListDataSource;

  let url = u;
  if (!url || Object.prototype.toString.call(url) !== '[object String]') {
    // eslint-disable-next-line prefer-destructuring
    url = req.url;
  }

  const params = (parse(url, true).query as unknown) as TableListParams;
  params.pageIndex = parseInt(params.pageIndex);
  params.pageSize = parseInt(params.pageSize);

  const startIndex: number = (params.pageIndex - 1) * params.pageSize
  const endIndex: number = startIndex + params.pageSize
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


export default {
  'GET /api/tag': getTagList,
};
