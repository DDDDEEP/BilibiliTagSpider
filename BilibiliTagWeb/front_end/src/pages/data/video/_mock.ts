// eslint-disable-next-line import/no-extraneous-dependencies
import moment from 'moment';
import { Request, Response } from 'express';
import { parse } from 'url';
import { TableListParams, VideoTableListItem } from './data.d';

// mock tableListDataSource
let tableListDataSource: VideoTableListItem[] = [];

for (let i = 0; i < 200; i += 1) {
  const randomPubdate: number = Math.round(Math.random() * 10000000000);
  tableListDataSource.push({
    tid: 17,
    pubdate: randomPubdate,
    aid: Math.round(Math.random() * 10000000),
    tags: '新手向,实况我打尼玛的,失落之船,饥荒,我打尼玛的我打尼玛的我打尼玛的',
    title: '车万车万车万车万车万车万车万车万车',
    duration: Math.round(Math.random() * 500000),
    stat_view: Math.round(Math.random() * 100000000),
    stat_danmaku: Math.round(Math.random() * 100000000),
    stat_reply: Math.round(Math.random() * 100000000),
    stat_favorite: Math.round(Math.random() * 100000000),
    stat_coin: Math.round(Math.random() * 100000000),
    stat_share: Math.round(Math.random() * 100000000),
    stat_like: Math.round(Math.random() * 100000000),
    stat_dislike: Math.round(Math.random() * 100000000),
    created_at: randomPubdate,
    updated_at: randomPubdate,
  });
}

function getVideoList(req: Request, res: Response, u: string) {
  let dataSource = tableListDataSource;

  let url = u;
  if (!url || Object.prototype.toString.call(url) !== '[object String]') {
    // eslint-disable-next-line prefer-destructuring
    url = req.url;
  }

  const params = (parse(url, true).query as unknown) as TableListParams;

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


export default {
  'GET /api/video': getVideoList,
};
