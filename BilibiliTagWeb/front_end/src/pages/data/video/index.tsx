import { Tag } from 'antd';
import React, { useState, useRef } from 'react';
import { PageHeaderWrapper } from '@ant-design/pro-layout';
import ProTable, { ProColumns, ActionType } from '@ant-design/pro-table';
import { VideoTableListItem } from './data.d';
import { getVideoList } from './service';
import { TYPE_ID_NAME, momentToTimestamp, secondsToStr } from '@/utils/utils';
import moment from 'moment';

const TableList: React.FC<{}> = () => {
  const actionRef = useRef<ActionType>();
  const columns: ProColumns<VideoTableListItem>[] = [
    {
      title: '标题',
      dataIndex: 'title',
      hideInSearch: true,
      width: 200,
    },
    {
      title: 'aid',
      dataIndex: 'aid',
      valueType: 'text',
      renderText: (val: number) => <a href={'https://www.bilibili.com/av' + val}>{val}</a>,
    },
    {
      title: '分区',
      dataIndex: 'tid',
      initialValue: '17',
      valueEnum: TYPE_ID_NAME,
      width: 130,
    },
    {
      title: '投稿时间',
      dataIndex: 'pubdate',
      valueType: 'dateRange',
      renderText: (val: number) => `${moment(val * 1000).format('YYYY-MM-DD HH:mm:ss')}`,
      width: 180,
    },
    {
      title: '标签',
      dataIndex: 'tags',
      hideInSearch: true,
      render: (_, record: VideoTableListItem) => (
        <>
          {record.tags.split(',').map((tag: string, index: number) => {
            return (
              <Tag key={index}>{tag}</Tag>
            );
          })}
        </>
      ),
      width: 250,
    },
    {
      title: '时长',
      dataIndex: 'duration',
      renderText: (val: number) => `${secondsToStr(val)}`,
      hideInSearch: true,
      width: 120,
    },
    {
      title: '播放量',
      dataIndex: 'stat_view',
      hideInSearch: true,
    },
    {
      title: '弹幕数',
      dataIndex: 'stat_danmaku',
      hideInSearch: true,
    },
    {
      title: '评论',
      dataIndex: 'stat_reply',
      hideInSearch: true,
    },
    {
      title: '收藏',
      dataIndex: 'stat_favorite',
      hideInSearch: true,
    },
    // {
    //   title: '硬币',
    //   dataIndex: 'stat_coin',
    //   hideInSearch: true,
    // },
    // {
    //   title: '分享',
    //   dataIndex: 'stat_share',
    //   hideInSearch: true,
    // },
    // {
    //   title: '点赞',
    //   dataIndex: 'stat_like',
    //   hideInSearch: true,
    // },
    
  ];

  return (
    <PageHeaderWrapper>
        <ProTable<VideoTableListItem>
          headerTitle="视频列表"
          actionRef={actionRef}
          rowKey="aid"
          toolBarRender={() => []}
          tableAlertRender={false}
          request={async (params: any) => {
            const pageIndex: number = params?.current ?? 1;
            const pageSize: number = params?.pageSize ?? 5;
            delete params?.current;
            delete params?.pageSize;
            delete params?._timestamp;
            if (params.tid == null) {
              params.tid = 17;
            }
            if (params.pubdate) {
              params.pubdate_min = momentToTimestamp(moment(params.pubdate[0]).startOf('day'));
              params.pubdate_max = momentToTimestamp(moment(params.pubdate[1]).endOf('day'));
              delete params.pubdate;
            }
            const data = await getVideoList({
              ...params,
              pageIndex: pageIndex,
              pageSize: pageSize,
            });
            return {
              data: data.data.results,
              total: data.data.count,
              pageSize: pageSize,
              current: pageIndex,
            };
          }}
          columns={columns}
          options={{
            density: false,
            fullScreen: false,
            reload: true,
            setting: false,
          }}
          pagination={{
            pageSize: 10,
            showTotal: (total, range) => `第 ${range[0]} - ${range[1]} 条/总共 ${total} 条`,
          }}
        />
    </PageHeaderWrapper>
  );
};

export default TableList;
