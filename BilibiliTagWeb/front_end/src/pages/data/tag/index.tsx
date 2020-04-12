import { Tag } from 'antd';
import React, { useState, useRef } from 'react';
import { PageHeaderWrapper } from '@ant-design/pro-layout';
import ProTable, { ProColumns, ActionType } from '@ant-design/pro-table';
import { TagTableListItem } from './data.d';
import { getTagList } from './service';
import { TYPE_ID_NAME, momentToTimestamp, secondsToStr } from '@/utils/utils';
import moment from 'moment';

const TableList: React.FC<{}> = () => {
  const actionRef = useRef<ActionType>();
  const columns: ProColumns<TagTableListItem>[] = [
    {
      title: '名字',
      dataIndex: 'name',
      render: (_, record: TagTableListItem) => (<Tag>{record.name}</Tag>),
      width: 200,
      align: 'center',
    },
  ];

  return (
    <PageHeaderWrapper>
        <ProTable<TagTableListItem>
          headerTitle="标签列表"
          actionRef={actionRef}
          rowKey="name"
          toolBarRender={() => []}
          tableAlertRender={false}
          request={async (params: any) => {
            const pageIndex: number = params?.current ?? 1;
            const pageSize: number = params?.pageSize ?? 5;
            delete params?.current;
            delete params?.pageSize;
            const data = await getTagList({
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
