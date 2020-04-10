import React, { useState, useRef, useEffect } from 'react';
import shortid from 'shortid';
import {
  Button,
  message,
  Progress,
  Calendar,
  Card,
  Row,
  Col,
  Select,
  Radio,
  Typography,
  Badge,
  DatePicker,
  Divider,
} from 'antd';
import moment from 'moment';
import { CalendarDataList, RecordListParams, RecordListItem } from '../data';
import styles from '../style.less';
import { RECORD_STATUS_VALUE, monthFixZero, momentToTimestamp, TYPE_ID_NAME } from '@/utils/utils';
import { getReocrdList } from '../service';

const { Option } = Select;

interface MonthCalendarProps {
  year: number;
  month: number;
  calendarData: CalendarDataList;
}

const MonthCalendar: React.FC<MonthCalendarProps> = (props) => {
  const { year: yearNum, month: monthNum, calendarData: calendarData } = props;
  const monthFirstDay = moment(`${yearNum}-${monthFixZero(monthNum)}-01`);
  const monthLastDay = moment(`${yearNum}-${monthFixZero(monthNum)}-01`).endOf('month');

  function dateCellRender(date: moment.Moment) {
    const timestamp = momentToTimestamp(date);
    const dates = monthFixZero(date.date());
    const hasStatus = calendarData.hasOwnProperty(timestamp);
    let classNames: string = styles.calendarDateText;
    if (hasStatus) {
      switch(calendarData[timestamp]) {
        case RECORD_STATUS_VALUE['Crawled']:
          classNames += ` ${styles.calendarDateTextCrawled}`;
          break;
        case RECORD_STATUS_VALUE['Handled']:
          classNames += ` ${styles.calendarDateTextHandled}`;
          break;
        case RECORD_STATUS_VALUE['Calculated']:
          classNames += ` ${styles.calendarDateTextCalculated}`;
          break;
        default:
          break;
      }
    }
    return (
      <label className={classNames}>{dates}</label>
    );
  }

  return (
    <Calendar
      value={monthFirstDay}
      validRange={[monthFirstDay, monthLastDay]}
      fullscreen={false}
      dateFullCellRender={dateCellRender}
      onSelect={() => {
        return false;
      }}
      headerRender={({ value, type, onChange, onTypeChange }) => {
        const title = `${yearNum}年${monthFixZero(monthNum)}月`;
        return (
          <div style={{ textAlign: 'center' }}>
            <Typography.Title level={4}>{title}</Typography.Title>
          </div>
        );
      }}
    />
  );
};

/**
 * 获取日历数据
 * @param params
 */
const getCalendarData = async (params: RecordListParams): Promise<RecordListItem[]> => {
  let data: RecordListItem[] = [];
  try {
    const response = await getReocrdList(params);
    if (response.status != 0) {
      message.error('日历数据出错');
    } else {
      data = response.data.results;
    }
  } catch (error) {
    message.error('日历数据请求失败');
  }
  return data;
};

const YearCalendar: React.FC<{}> = () => {
  const [calendarTid, setCalendarTid] = useState<number>(17);
  const [calendarYear, setCalendarYear] = useState<number>(moment().year());
  const [calendarData, setCalendarData] = useState<CalendarDataList>({});

  // 刷新日历
  const reloadCalendar = async () => {
    let newCalendarData = {};
    const records = await getCalendarData({
      tid: calendarTid,
      pubdate_min: momentToTimestamp(moment(`${calendarYear}-01-01`)),
      pubdate_max: momentToTimestamp(moment(`${calendarYear}-12-31`)),
      pageIndex: 1,
      pageSize: 366,
    });
    records.forEach((value: RecordListItem) => {
      newCalendarData[value.pubdate] = value.status;
    });
    setCalendarData(newCalendarData);
  };

  useEffect(() => {
    reloadCalendar();
    const calendarReloadTimer = setInterval(() => {
      reloadCalendar();
    }, 10000);

    return () => clearInterval(calendarReloadTimer);
  }, [calendarTid, calendarYear]);

  return (
    <>
      <Row gutter={[16, 16]}>
        <Col span={6}>
          <b>分区：</b>
          <Select defaultValue='17' placeholder="请选择分区" style={{ width: 200 }}
            onChange={(value: string) => {
              setCalendarTid(parseInt(value));
            }}
          >
            {Object.keys(TYPE_ID_NAME).map((key: string) => {
              return (
                <Option key={key} value={key}>
                  {key}: {TYPE_ID_NAME[key]}
                </Option>
              );
            })}
          </Select>
        </Col>
        <Col span={6}>
          <b>年份：</b>
          <DatePicker picker="year" allowClear={false} defaultValue={moment()}
            onChange={(value: moment.Moment | null) => {
              setCalendarYear(value ? value.year() : 2000);
            }}
          />
        </Col>
        <Col span={6} offset={6}>
          <label className={`${styles.calendarDateText} ${styles.calendarDateTextCrawled}`}>已爬取</label>
          <Divider type="vertical" />
          <label className={`${styles.calendarDateText} ${styles.calendarDateTextHandled}`}>已处理标签</label>
          <Divider type="vertical" />
          <label className={`${styles.calendarDateText} ${styles.calendarDateTextCalculated}`}>已计算数据</label>
        </Col>
      </Row>
      <Row>
        <Col className={styles.calendarContainer} span={6}>
          <MonthCalendar year={calendarYear} month={1} calendarData={calendarData} />
        </Col>
        <Col className={styles.calendarContainer} span={6}>
          <MonthCalendar year={calendarYear} month={2} calendarData={calendarData} />
        </Col>
        <Col className={styles.calendarContainer} span={6}>
          <MonthCalendar year={calendarYear} month={3} calendarData={calendarData} />
        </Col>
        <Col className={styles.calendarContainer} span={6}>
          <MonthCalendar year={calendarYear} month={4} calendarData={calendarData} />
        </Col>
        <Col className={styles.calendarContainer} span={6}>
          <MonthCalendar year={calendarYear} month={5} calendarData={calendarData} />
        </Col>
        <Col className={styles.calendarContainer} span={6}>
          <MonthCalendar year={calendarYear} month={6} calendarData={calendarData} />
        </Col>
        <Col className={styles.calendarContainer} span={6}>
          <MonthCalendar year={calendarYear} month={7} calendarData={calendarData} />
        </Col>
        <Col className={styles.calendarContainer} span={6}>
          <MonthCalendar year={calendarYear} month={8} calendarData={calendarData} />
        </Col>
        <Col className={styles.calendarContainer} span={6}>
          <MonthCalendar year={calendarYear} month={9} calendarData={calendarData} />
        </Col>
        <Col className={styles.calendarContainer} span={6}>
          <MonthCalendar year={calendarYear} month={10} calendarData={calendarData} />
        </Col>
        <Col className={styles.calendarContainer} span={6}>
          <MonthCalendar year={calendarYear} month={11} calendarData={calendarData} />
        </Col>
        <Col className={styles.calendarContainer} span={6}>
          <MonthCalendar year={calendarYear} month={12} calendarData={calendarData} />
        </Col>
      </Row>
    </>
  )
}
export default YearCalendar;
