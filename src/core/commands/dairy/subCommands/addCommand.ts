import { CommandType } from "../../../command";
import { defineAsyncComponent } from "vue";
import ComponentOutputType = YuTerminal.ComponentOutputType;

const addCommand: CommandType = {
  func: "add",
  name: "添加日记",
  options: [],
  action(options, terminal) {
    const { _ } = options;
    if (_.length < 1) {
      const output: ComponentOutputType = {
        type: "component",
        component: defineAsyncComponent(() => import("../DairyEditorBox.vue")),
      };
      terminal.writeResult(output);
      return;
    }
  },
};

export default addCommand;
