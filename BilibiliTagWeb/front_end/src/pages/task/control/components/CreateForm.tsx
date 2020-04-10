import moment from 'moment';
import React from 'react';
import { Form, Input, Modal, Select, DatePicker } from 'antd';

import { TaskTableListItem } from '../data.d';
import { TASK_TYPE_NAME, TYPE_ID_NAME } from '@/utils/utils';

const { Option } = Select;
const FormItem = Form.Item;
const { RangePicker } = DatePicker;

export interface FormValueType {
  task_type?: number;
  tid?: number;
  time?: moment.Moment[];
}

interface CreateFormProps {
  modalVisible: boolean;
  onSubmit: (values: FormValueType) => void;
  onCancel: () => void;
}

const CreateForm: React.FC<CreateFormProps> = (props) => {
  const [form] = Form.useForm();

  const { modalVisible, onSubmit: handleAdd, onCancel } = props;
  const okHandle = async () => {
    const fieldsValue = await form.validateFields();
    form.resetFields();
    handleAdd(fieldsValue);
  };
  return (
    <Modal
      destroyOnClose
      title="新建任务"
      visible={modalVisible}
      onOk={okHandle}
      onCancel={() => onCancel()}
    >
      <Form form={form}>
        <FormItem
          name="task_type"
          label="类型"
          rules={[{ required: true, message: '请选择任务类型' }]}
        >
          <Select placeholder="请选择任务类型">
            {Object.keys(TASK_TYPE_NAME).map((key: string) => {
              return <Option key={key} value={key}>{TASK_TYPE_NAME[key]}</Option>;
            })}
          </Select>
        </FormItem>
        <FormItem name="tid" label="分区" rules={[{ required: true, message: '请选择分区' }]}>
          <Select placeholder="请选择分区">
            {Object.keys(TYPE_ID_NAME).map((key: string) => {
              return (
                <Option key={key} value={key}>
                  {key}: {TYPE_ID_NAME[key]}
                </Option>
              );
            })}
          </Select>
        </FormItem>
        <FormItem
          name="time"
          label="时间"
          rules={[{ required: true, message: '请选择时间范围' }]}
        >
          <RangePicker />
        </FormItem>
      </Form>
    </Modal>
  );
};

export default CreateForm;
