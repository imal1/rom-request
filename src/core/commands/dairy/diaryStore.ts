import { defineStore } from "pinia";
import DiaryType = Diary.DiaryType;

export const useDiaryStore = defineStore("diary", {
  state: () => ({
    diaryList: [] as DiaryType[],
  }),
  getters: {},
  // 持久化
  persist: {
    key: "diary-store",
    storage: window.localStorage,
    beforeRestore: (context) => {
      console.log("load diaryStore data start");
    },
    afterRestore: (context) => {
      console.log("load diaryStore data end");
    },
  },
  actions: {
    /**
     * 创建日记
     * @param diary
     */
    addDiary(diary: DiaryType) {
      if (!diary || !diary.name) {
        return false;
      }
      diary.isFinished = false;
      diary.createTime = new Date();
      this.diaryList.push(diary);
      return true;
    },
    /**
     * 删除日记
     * @param index
     */
    deleteDiary(index: number) {
      if (index < 0 || index >= this.diaryList.length) {
        return false;
      }
      this.diaryList.splice(index, 1);
      return true;
    },
    /**
     * 更新日记
     * @param index
     * @param newDiary
     */
    updateDiary(index: number, newDiary: DiaryType) {
      if (index < 0 || index >= this.diaryList.length) {
        return false;
      }
      this.diaryList[index] = { ...this.diaryList[index], ...newDiary };
    },
  },
});
