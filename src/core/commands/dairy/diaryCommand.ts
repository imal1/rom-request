import { CommandType } from "../../command";
import { defineAsyncComponent } from "vue";
import ComponentOutputType = YuTerminal.ComponentOutputType;
import addCommand from "./subCommands/addCommand";

const diaryCommand: CommandType = {
  func: "diary",
  name: "日记本",
  desc: "打开日记列表或每日一篇",
  params: [
    {
      key: "subCommand",
      desc: "子命令",
      required: true,
    },
  ],
  options: [],
  subCommands: {
    add: addCommand,
  },
  collapsible: true,
  action(options, terminal) {
    const { _ } = options;
    if (_.length < 1) {
      const output: ComponentOutputType = {
        type: "component",
        component: defineAsyncComponent(() => import("./DairyBox.vue")),
      };
      terminal.writeResult(output);
      return;
    }
  },
};

export default diaryCommand;
