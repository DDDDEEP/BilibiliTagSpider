import moment, { Moment } from 'moment';
import shortid from 'shortid';
import { DownOutlined, PlusOutlined } from '@ant-design/icons';
import { Button, message, Progress, Calendar, Card, Row, Col, Select, DatePicker } from 'antd';
import React, { useState, useRef, useEffect } from 'react';
import { PageHeaderWrapper } from '@ant-design/pro-layout';
import ProTable, { ProColumns, ActionType } from '@ant-design/pro-table';
import CreateForm, { FormValueType } from './components/CreateForm';
import YearCalendar from './components/YearCalendar';
import {
  TaskTableListItem,
  TaskProgress,
  TaskStartParams,
  RecordListItem,
  RecordListParams,
  CalendarDataList,
} from './data.d';
import { getTaskList, startSpider, startHandler, getReocrdList } from './service';
import styles from './style.less';
import { TASK_TYPE_NAME, TYPE_ID_NAME, momentToTimestamp } from '@/utils/utils';

const { Option } = Select;

/**
 * 创建异步任务
 * @param fields
 */
const handleAdd = async (fields: FormValueType) => {
  const hide = message.loading('正在创建任务');
  try {
    if (fields.task_type && fields.tid && fields.time) {
      const params: TaskStartParams = {
        tid: fields.tid,
        from: parseInt(fields.time[0].format('YYYYMMDD')),
        to: parseInt(fields.time[1].format('YYYYMMDD')),
      };
      hide();
      let response;
      if (fields.task_type == 0) {
        response = await startSpider(params);
      } else {
        response = await startHandler(params);
      }

      if (response.status == 0) {
        message.success('任务创建成功');
      } else {
        message.error(response.message);
      }
    }
    return true;
  } catch (error) {
    hide();
    message.error('创建失败，请重试');
    return false;
  }
};

const TableList: React.FC<{}> = () => {
  const [createModalVisible, handleModalVisible] = useState<boolean>(false);
  const actionRef = useRef<ActionType>();

  // 定时刷新表格
  useEffect(() => {
    const tableReloadTimer = setInterval(() => {
      if (actionRef.current) {
        actionRef.current.reload();
      }
    }, 5000);

    return () => clearInterval(tableReloadTimer);
  }, []);

  const columns: ProColumns<TaskTableListItem>[] = [
    {
      title: '任务类型',
      dataIndex: 'task_type',
      renderText: (val: number) => `${TASK_TYPE_NAME[val]}`,
    },
    {
      title: '分区',
      dataIndex: 'tid',
      renderText: (val: number) => `${TYPE_ID_NAME[val]}`,
    },
    {
      title: '时间范围',
      renderText: (_, record) =>
        `${moment(record.time_from.toString()).format('YYYY-MM-DD')} ~ ${moment(record.time_to.toString()).format(
          'YYYY-MM-DD',
        )}`,
    },
    {
      title: '状态',
      dataIndex: 'state',
      valueEnum: {
        PENDING: { text: '未知', status: 'Default' },
        STARTED: { text: '已开始', status: 'Warning' },
        PROGRESS: { text: '进行中', status: 'Processing' },
        SUCCESS: { text: '已完成', status: 'Success' },
        ERROR: { text: '异常', status: 'Error' },
      },
    },
    {
      title: '进度',
      dataIndex: 'progress',
      width: 400,
      render: (_, record: TaskTableListItem) => (
        <>
          {record.progress.map((progress: TaskProgress) => {
            const percent: number =
              progress.total == 0 ? 0 : Math.round((progress.cur / progress.total) * 100);
            return (
              <Progress
                style={{ width: 200 }}
                percent={percent}
                status={percent == 100 ? 'success' : 'active'}
                strokeWidth={6}
                key={shortid.generate()}
                format={(percent) => `${percent}%, (${progress.cur}/${progress.total})`}
              />
            );
          })}
        </>
      ),
    },
    {
      title: '开始时间',
      dataIndex: 'time_start',
      renderText: (val: number) => `${moment(val * 1000).format('YYYY-MM-DD HH:mm:ss')}`,
    },
    {
      title: '结束时间',
      dataIndex: 'time_end',
      renderText: (val: number) =>
        `${val == -1 ? '--' : moment(val * 1000).format('YYYY-MM-DD HH:mm:ss')}`,
    },
  ];
  return (
    <PageHeaderWrapper>
      <Card title="任务列表" style={{ marginBottom: 24 }} bordered={false}>
        <ProTable<TaskTableListItem>
          actionRef={actionRef}
          rowKey="task_id"
          toolBarRender={() => [
            <Button icon={<PlusOutlined />} type="primary" onClick={() => handleModalVisible(true)}>
              新建任务
            </Button>,
          ]}
          tableAlertRender={false}
          request={async (params) => {
            const pageIndex: number = params?.current ?? 1;
            const pageSize: number = params?.pageSize ?? 5;
            delete params?.current;
            delete params?.pageSize;
            const data = await getTaskList({
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
          search={false}
          pagination={{
            pageSize: 5,
            showTotal: (total, range) => `第 ${range[0]} - ${range[1]} 条/总共 ${total} 条`,
          }}
        />
        <CreateForm
          onSubmit={async (value) => {
            const success = await handleAdd(value);
            if (success) {
              handleModalVisible(false);
              if (actionRef.current) {
                actionRef.current.reload();
              }
            }
          }}
          onCancel={() => handleModalVisible(false)}
          modalVisible={createModalVisible}
        />
      </Card>
      <Card title="已爬取记录" style={{ marginBottom: 24 }} bordered={true}>
        <YearCalendar />
      </Card>
    </PageHeaderWrapper>
  );
};

export default TableList;
