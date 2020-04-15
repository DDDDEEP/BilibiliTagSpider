export interface TagAvgStatTableListItem {
  total_count: number;
  tag_name: string;
  avg_stat: number;
}

export interface TableListPagination {
  total: number;
  pageSize: number;
  current: number;
}

export interface TableListData {
  list: VideoTableListItem[];
  pagination: Partial<TableListPagination>;
}

export interface TableListParams {
  tid?: number;
  count?: number;
  stat_code?: number;
  min_tag_count?: number;
  pageIndex: number;
  pageSize: number;
}
