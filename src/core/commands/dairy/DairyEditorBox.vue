<template>
  <div style="margin: 8px 0; max-width: 800px">
    <Toolbar
      style="border-bottom: 1px solid #ccc"
      :editor="editorRef"
      :default-config="toolbarConfig"
      :mode="mode"
    />
    <Editor
      v-model="valueHtml"
      style="height: 500px; overflow-y: hidden"
      :default-config="editorConfig"
      :mode="mode"
      @onCreated="handleCreated"
    />
  </div>
</template>
<script setup lang="ts">
import "@wangeditor/editor/dist/css/style.css";
import { shallowRef, toRefs } from "vue";
import type { ShallowRef } from "vue";
import { IDomEditor } from "@wangeditor/editor";
import { Editor, Toolbar } from "@wangeditor/editor-for-vue";

interface EditorBoxProps {
  mode: string;
  editorRef: ShallowRef;
  toolbarConfig: object;
  valueHtml: string;
  editorConfig: object;
}

const props = withDefaults(defineProps<EditorBoxProps>(), {});
const {
  mode = "default",
  editorRef = shallowRef(),
  toolbarConfig,
  editorConfig = { placeholder: "请输入内容..." },
  valueHtml = "",
} = toRefs(props);

const handleCreated = (editor: IDomEditor) => {
  editorRef.value = editor;
};
</script>
