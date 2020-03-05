<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 基础表格
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div class="handle-box">
        <el-input v-model="query.name"
                  placeholder="视频名"
                  class="handle-input mr10"></el-input>
        <el-button type="primary"
                   icon="el-icon-search"
                   @click="handleSearch">搜索</el-button>
      </div>
      <el-table :data="tableData"
                border
                class="table"
                ref="multipleTable"
                header-cell-class-name="table-header"
                @selection-change="handleSelectionChange">
        <!-- <el-table-column type="selection"
                         width="55"
                         align="center"></el-table-column> -->
        <el-table-column prop="tid"
                         label="分区号"
                         width="80"
                         align="center"></el-table-column>
        <el-table-column prop="title"
                         label="标题"></el-table-column>
        <el-table-column label="AV号"
                         width="110"
                         align="center">
          <template slot-scope="scope"><a :href="'https://www.bilibili.com/video/av' + scope.row.aid"
               target="_blank">av{{scope.row.aid}}</a></template>
        </el-table-column>
        <el-table-column label="时长"
                         width="90"
                         align="right">
          <template slot-scope="scope">{{scope.row.duration}}分钟</template>
        </el-table-column>
        <el-table-column label="发布日期"
                         width="170"
                         align="center">
          <template slot-scope="scope">{{scope.row.pubdate | formatDate}}</template>
        </el-table-column>
        <el-table-column prop="stat_view"
                         label="播放量"
                         width="80"
                         align="right"></el-table-column>
        <el-table-column prop="stat_danmaku"
                         label="弹幕数"
                         width="80"
                         align="right"></el-table-column>
        <el-table-column prop="stat_reply"
                         label="评论"
                         width="80"
                         align="right"></el-table-column>
        <el-table-column prop="stat_favorite"
                         label="收藏"
                         width="80"
                         align="right"></el-table-column>
        <!-- <el-table-column prop="stat_coin"
                         label="硬币"
                         width="80"
                         align="right"></el-table-column> -->
        <el-table-column prop="tags"
                         label="标签"
                         align="left"></el-table-column>

      </el-table>
      <div class="pagination">
        <el-pagination background
                       layout="total, prev, pager, next"
                       :current-page="query.pageIndex"
                       :page-size="query.pageSize"
                       :total="pageTotal"
                       @current-change="handlePageChange"></el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchData } from '../../api/index';
export default {
  name: 'basetable',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 10,
        tid: 17,
      },
      tableData: [],
      multipleSelection: [],
      delList: [],
      editVisible: false,
      pageTotal: 0,
      form: {},
      idx: -1,
      id: -1,
      tid: 17,
    };
  },
  created () {
    this.getData();
  },
  methods: {
    // 获取数据
    getData () {
      fetchData(this.query).then(res => {
        this.tableData = res.data.results;
        this.pageTotal = res.data.count;
      });
    },
    // 触发搜索按钮
    handleSearch () {
      this.$set(this.query, 'pageIndex', 1);
      this.getData();
    },
    // 删除操作
    handleDelete (index, row) {
      // 二次确认删除
      this.$confirm('确定要删除吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          this.$message.success('删除成功');
          this.tableData.splice(index, 1);
        })
        .catch(() => { });
    },
    // 多选操作
    handleSelectionChange (val) {
      this.multipleSelection = val;
    },
    delAllSelection () {
      const length = this.multipleSelection.length;
      let str = '';
      this.delList = this.delList.concat(this.multipleSelection);
      for (let i = 0; i < length; i++) {
        str += this.multipleSelection[i].name + ' ';
      }
      this.$message.error(`删除了${str}`);
      this.multipleSelection = [];
    },
    // 编辑操作
    handleEdit (index, row) {
      this.idx = index;
      this.form = row;
      this.editVisible = true;
    },
    // 保存编辑
    saveEdit () {
      this.editVisible = false;
      this.$message.success(`修改第 ${this.idx + 1} 行成功`);
      this.$set(this.tableData, this.idx, this.form);
    },
    // 分页导航
    handlePageChange (val) {
      this.$set(this.query, 'pageIndex', val);
      this.getData();
    }
  },
  filters: {
    formatDate: function (value) {// 格式化时间戳
      if (value == null) {
        return '';
      } else {
        let date = new Date(value * 1000);
        let y = date.getFullYear();// 年
        let MM = date.getMonth() + 1;// 月
        MM = MM < 10 ? ('0' + MM) : MM;
        let d = date.getDate();// 日
        d = d < 10 ? ('0' + d) : d;
        let h = date.getHours();// 时
        h = h < 10 ? ('0' + h) : h;
        let m = date.getMinutes();// 分
        m = m < 10 ? ('0' + m) : m;
        let s = date.getSeconds();// 秒
        s = s < 10 ? ('0' + s) : s;
        return y + '-' + MM + '-' + d + ' ' + h + ':' + m + ':' + s;
      }
    }
  }
};
</script>

<style scoped>
.handle-box {
    margin-bottom: 20px;
}

.handle-select {
    width: 120px;
}

.handle-input {
    width: 300px;
    display: inline-block;
}
.table {
    width: 100%;
    font-size: 14px;
}
.red {
    color: #ff0000;
}
.mr10 {
    margin-right: 10px;
}
.table-td-thumb {
    display: block;
    margin: auto;
    width: 40px;
    height: 40px;
}
</style>
