export interface TaskTableListItem {
  task_id: string;
  task_type: number;
  tid: number;
  time_from: number;
  time_to: number;
  time_start: number;
  time_end: number;
  state: 'PENDING' | 'STARTED' | 'PROGRESS' | 'SUCCESS' | 'ERROR';
  progress: TaskProgress[];
  extra: TaskExtraInfo;
}

export interface TaskProgress {
  cur: number;
  total: number;
}

export interface TaskExtraInfo {
  status?: number;
}

export interface ListPagination {
  total: number;
  pageSize: number;
  current: number;
}

export interface TaskTableListData {
  list: TaskTableListItem[];
  pagination: Partial<TableListPagination>;
}

export interface TableListParams {
  pageIndex: number;
  pageSize: number;
}

export interface TaskStartParams {
  tid: number;
  from: number;
  to: number;
}

export interface RecordListItem {
  tid: number;
  pubdate: number;
  status: number;
}

export interface RecordListParams {
  tid: number;
  pubdate_min: number;
  pubdate_max: number;
  pageIndex: number;
  pageSize: number;
}

export interface CalendarDataList {
  [key: number]: number;
}
