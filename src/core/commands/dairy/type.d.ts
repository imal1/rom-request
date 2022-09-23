declare namespace Diary {
  /**
   * 任务类型
   */
  interface DiaryType {
    name: string;
    isFinished: boolean;
    createTime: date;
    finishTime?: date;
  }
}
