export interface TagCountTableListItem {
  sum_count: number;
  tag_name: string;
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
  pageIndex: number;
  pageSize: number;
}
