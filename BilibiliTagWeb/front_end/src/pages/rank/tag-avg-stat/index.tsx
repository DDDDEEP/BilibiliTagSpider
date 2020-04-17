import { message, Tag } from 'antd';
import React, { useState, useRef } from 'react';
import { PageHeaderWrapper } from '@ant-design/pro-layout';
import ProTable, { ProColumns, ActionType } from '@ant-design/pro-table';
import { TagAvgStatTableListItem } from './data.d';
import { getTagAvgStattList } from './service';
import { TYPE_ID_NAME, VIDEO_STAT_NAME, momentToTimestamp, secondsToStr } from '@/utils/utils';
import moment from 'moment';

const TableList: React.FC<{}> = () => {
  const actionRef = useRef<ActionType>();
  const columns: ProColumns<TagAvgStatTableListItem>[] = [
    {
      title: '分区',
      dataIndex: 'tid',
      hideInTable: true,
      initialValue: '17',
      valueEnum: TYPE_ID_NAME,
    },
    {
      title: '数据项',
      dataIndex: 'stat_code',
      hideInTable: true,
      initialValue: '0',
      valueEnum: VIDEO_STAT_NAME,
    },
    {
      title: '投稿时间',
      dataIndex: 'pubdate',
      hideInTable: true,
      valueType: 'dateRange',
      renderText: (val: number) => `${moment(val * 1000).format('YYYY-MM-DD HH:mm:ss')}`,
    },
    {
      title: '排名数',
      dataIndex: 'count',
      hideInTable: true,
      initialValue: '10',
      valueEnum: {
        '10': '10',
        '20': '20',
        '30': '30',
      },
    },
    {
      title: '最小标签出现次数',
      dataIndex: 'min_tag_count',
      hideInTable: true,
      initialValue: 10,
    },
    {
      title: '排名',
      dataIndex: 'index',
      valueType: 'indexBorder',
      align: 'center',
    },
    {
      title: '标签名',
      dataIndex: 'tag_name',
      hideInSearch: true,
      render: (_, record: TagAvgStatTableListItem) => (<Tag style={{fontSize: 16}}>{record.tag_name}</Tag>),
      align: 'center',
    },
    {
      title: '平均数据',
      dataIndex: 'avg_stat',
      hideInSearch: true,
      align: 'center',
    },
    {
      title: '标签出现次数',
      dataIndex: 'sum_count',
      hideInSearch: true,
      align: 'center',
    },
  ];

  return (
    <PageHeaderWrapper>
        <ProTable<TagAvgStatTableListItem>
          headerTitle="排行列表"
          actionRef={actionRef}
          rowKey="tag_name"
          toolBarRender={() => []}
          tableAlertRender={false}
          request={async (params: any) => {
            delete params?.current;
            delete params?.pageSize;
            delete params?._timestamp;
            if (params.tid == null) {
              params.tid = 17;
            }
            if (params.pubdate) {
              params.from = moment(params.pubdate[0]).format('YYYYMMDD');
              params.to = moment(params.pubdate[1]).format('YYYYMMDD');
              delete params.pubdate;
            }
            const data = await getTagAvgStattList({
              ...params,
            });
            if (data.status == 1) {
              message.error(data.message);
            } 
            return {
              data: data.data.result,
            };
          }}
          columns={columns}
          options={{
            density: false,
            fullScreen: false,
            reload: true,
            setting: false,
          }}
          pagination={false}
          search = {{collapsed: false,}}
        />
    </PageHeaderWrapper>
  );
};

export default TableList;
