export interface VideoTagTableListItem {
  _id: string;
  tid: number;
  pubdate: number;
  tag_id: string;
  aids: string;
  avg_stat_view: number;
  avg_stat_danmaku: number;
  avg_stat_reply: number;
  avg_stat_favorite: number;
  avg_stat_coin: number;
  avg_stat_share: number;
  avg_stat_like: number;
  avg_stat_dislike: number;
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
  pubdate_min?: number;
  pubdate_max?: number;
  tag_id?: string;
  pageIndex: number;
  pageSize: number;
}

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

export interface VideoTableListParams {
  tag_tid?: number;
  tag_pubdate: number;
  tag_name?: string;
  pageIndex: number;
  pageSize: number;
}