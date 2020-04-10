export interface VideoTableListItem {
  tid: number;
  pubdate: number,
  aid: number,
  tags: string,
  title: string,
  duration: number,
  stat_view: number;
  stat_danmaku: number;
  stat_reply: number;
  stat_favorite: number;
  stat_coin: number;
  stat_share: number;
  stat_like: number;
  stat_dislike: number;
  created_at: number;
  updated_at: number;
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
  aid?: number;
  pubdate_min?: number;
  pubdate_max?: number;
  pageIndex: number;
  pageSize: number;
}
