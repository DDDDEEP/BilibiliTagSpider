import { Tag, Card, DatePicker, Select, message } from 'antd';
import React, { useState, useRef, ChangeEvent } from 'react';
import { PageHeaderWrapper } from '@ant-design/pro-layout';
import ProTable, { ProColumns, ActionType } from '@ant-design/pro-table';
import { VideoTagTableListItem, VideoTableListItem } from './data.d';
import { getVideoTagList, getVideoListByTag } from './service';
import { TYPE_ID_NAME, momentToTimestamp, secondsToStr } from '@/utils/utils';
import moment from 'moment';
import { FormInstance } from 'antd/lib/form';

const TableList: React.FC<{}> = () => {
  const videoTagActionRef = useRef<ActionType>();
  const videoActionRef = useRef<ActionType>();
  const videoFromRef = useRef<FormInstance>();
  const videoCardRef = useRef(null)
  const columns: ProColumns<VideoTagTableListItem>[] = [
    {
      title: '分区',
      dataIndex: 'tid',
      initialValue: '17',
      valueEnum: TYPE_ID_NAME,
      width: 150,
    },
    {
      title: '投稿日期',
      dataIndex: 'pubdate',
      valueType: 'dateRange',
      renderText: (val: number) => `${moment(val * 1000).format('YYYY-MM-DD')}`,
      width: 130,
    },
    {
      title: '标签名',
      dataIndex: 'tag_id',
      render: (_, record: VideoTagTableListItem) => (<Tag style={{fontSize: 16}}>{record.tag_id}</Tag>),
      width: 150,
    },
    {
      title: '视频列表',
      dataIndex: 'aids',
      hideInSearch: true,
      render: (_, record: VideoTagTableListItem) => (
        <>
          {JSON.parse(record.aids).map((aid: number, index: number) => {
            return (
              <label key={aid}>
                <a href={'https://www.bilibili.com/av' + aid}>{aid}</a>
                {index % 5 == 4 &&
                  <br />
                }
              </label>
            )
          })}
        </>
      ),
      width: 180,
    },
    {
      title: '平均播放',
      dataIndex: 'avg_stat_view',
      hideInSearch: true,
    },
    {
      title: '平均弹幕',
      dataIndex: 'avg_stat_danmaku',
      hideInSearch: true,
    },
    {
      title: '平均评论',
      dataIndex: 'avg_stat_reply',
      hideInSearch: true,
    },
    {
      title: '平均硬币',
      dataIndex: 'avg_stat_coin',
      hideInSearch: true,
    },
    {
      title: '平均分享',
      dataIndex: 'avg_stat_share',
      hideInSearch: true,
    },
    {
      title: '平均点赞',
      dataIndex: 'avg_stat_like',
      hideInSearch: true,
    },
    {
      title: '操作',
      key: 'action',
      render: (text, record) => (
        <a
          onClick={() => {
            if (videoCardRef != null && videoFromRef.current != null) {
              videoFromRef.current.setFieldsValue({
                'tid': record.tid.toString(),
                'pubdate': moment(record.pubdate * 1000),
                'tags': record.tag_id,
              });
              videoFromRef.current.submit();
              message.success('单日视频列表已更新')
            }
          }}
        >
          详情
        </a>
      ),
      width: 80
    },
  ];

  const videoColumns: ProColumns<VideoTableListItem>[] = [
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
      hideInSearch: true,
      renderText: (val: number) => <a href={'https://www.bilibili.com/av' + val}>{val}</a>,
    },
    {
      title: '分区',
      dataIndex: 'tid',
      valueEnum: TYPE_ID_NAME,
      width: 130,
    },
    {
      title: '投稿时间',
      dataIndex: 'pubdate',
      valueType: 'dateTime',
      renderText: (val: number) => `${moment(val * 1000).format('YYYY-MM-DD HH:mm:ss')}`,
      renderFormItem: (item, props)=> {
        return (
          <DatePicker {...props}/>
        )
      },
      width: 180,
    },
    {
      title: '标签',
      dataIndex: 'tags',
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
      title: '硬币',
      dataIndex: 'stat_coin',
      hideInSearch: true,
    },
    {
      title: '分享',
      dataIndex: 'stat_share',
      hideInSearch: true,
    },
    {
      title: '点赞',
      dataIndex: 'stat_like',
      hideInSearch: true,
    },
    
  ];

  return (
    <PageHeaderWrapper>
      <Card title="" style={{ marginBottom: 24 }} bordered={false}>
        <ProTable<VideoTagTableListItem>
          headerTitle="单日对应标签的数据列表"
          actionRef={videoTagActionRef}
          rowKey='_id'
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
              params.pubdate_max = momentToTimestamp(moment(params.pubdate[1]).startOf('day'));
              delete params.pubdate;
            }
            const data = await getVideoTagList({
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
            pageSize: 5,
            showTotal: (total, range) => `第 ${range[0]} - ${range[1]} 条/总共 ${total} 条`,
          }}
        />
      </Card>
      
      <Card ref={videoCardRef} title="" style={{ marginBottom: 24 }} bordered={true}>
        <ProTable<VideoTableListItem>
          id='video-table'
          headerTitle='单日对应标签的视频列表'
          actionRef={videoActionRef}
          rowKey='aid'
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
              params.tag_pubdate = momentToTimestamp(moment(params.pubdate).startOf('day'));
              delete params.pubdate;
            }
            if (params.tags) {
              params.tag_name = params.tags;
              delete params.tags;
            }
            const data = await getVideoListByTag({
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
          columns={videoColumns}
          options={{
            density: false,
            fullScreen: false,
            reload: true,
            setting: false,
          }}
          formRef={videoFromRef}
          pagination={{
            pageSize: 10,
            showTotal: (total, range) => `第 ${range[0]} - ${range[1]} 条/总共 ${total} 条`,
          }}
        />
      </Card>
    </PageHeaderWrapper>
  );
};

export default TableList;
